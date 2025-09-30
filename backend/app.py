import base64
import json
import os
import uuid
from flask import Flask, jsonify, redirect, request, session, url_for
from flask_cors import CORS
from flask_session import Session
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173", "https://eve-project-manager.onrender.com"])

# --- Configuration ---
# Load application settings from the external JSON file
try:
    with open(os.path.join(os.path.dirname(__file__), '..', 'Application Settings.json'), 'r') as f:
        app_settings = json.load(f)
except FileNotFoundError:
    print("FATAL: Application Settings.json not found.")
    exit()

CLIENT_ID = app_settings.get("clientId")
CLIENT_SECRET = app_settings.get("clientSecret")
CALLBACK_URL = app_settings.get("callbackUrl")
SCOPES_STRING = ' '.join(app_settings.get("scopes", []))
CHARACTERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'characters.json')

# Configure session to use filesystem (server-side)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.urandom(24)  # Use a random secret key
Session(app)

# --- Helper Functions ---
def load_characters():
    """Loads characters from the characters.json file."""
    if not os.path.exists(CHARACTERS_FILE):
        return []
    try:
        with open(CHARACTERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_characters(characters):
    """Saves the characters list to the characters.json file."""
    with open(CHARACTERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(characters, f, indent=4)

# --- SSO Routes ---
@app.route('/sso/login')
def sso_login():
    """
    Redirects the user to the EVE Online SSO authorization page.
    """
    state = str(uuid.uuid4())
    session['sso_state'] = state

    sso_url = (
        "https://login.eveonline.com/v2/oauth/authorize/?"
        "response_type=code"
        f"&redirect_uri={CALLBACK_URL}"
        f"&client_id={CLIENT_ID}"
        f"&scope={SCOPES_STRING}"
        f"&state={state}"
    )
    return redirect(sso_url)

@app.route('/callback')
def sso_callback():
    """
    Handles the callback from EVE SSO after user authorization.
    """
    code = request.args.get('code')
    state = request.args.get('state')

    # 1. Validate state to prevent CSRF
    if 'sso_state' not in session or state != session.pop('sso_state'):
        return "Error: State mismatch. CSRF attack suspected.", 400

    # 2. Exchange authorization code for tokens
    try:
        auth_header_value = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        token_response = requests.post(
            "https://login.eveonline.com/v2/oauth/token",
            headers={
                "Authorization": f"Basic {auth_header_value}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "login.eveonline.com"
            },
            data={
                "grant_type": "authorization_code",
                "code": code
            }
        )
        token_response.raise_for_status()
        tokens = token_response.json()
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']

        # 3. Verify token to get character information
        verify_response = requests.get(
            "https://login.eveonline.com/oauth/verify",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        verify_response.raise_for_status()
        char_data = verify_response.json()
        character_id = char_data['CharacterID']
        character_name = char_data['CharacterName']

        # 4. Save character data
        characters = load_characters()
        # Check if character already exists and update tokens, otherwise add new
        char_found = False
        for char in characters:
            if char['character_id'] == character_id:
                char['access_token'] = access_token
                char['refresh_token'] = refresh_token
                char_found = True
                break

        if not char_found:
            characters.append({
                "character_id": character_id,
                "name": character_name,
                "access_token": access_token,
                "refresh_token": refresh_token
            })

        save_characters(characters)

        # 5. Redirect to the frontend application
        return redirect("https://eve-project-manager.onrender.com/home")

    except requests.RequestException as e:
        print(f"Error during SSO callback: {e}")
        return "Error: Could not retrieve tokens or verify character.", 500

# --- API Routes ---
@app.route('/')
def hello_world():
    return 'Hello, from the backend!'

@app.route('/characters')
def get_characters():
    """
    Gets the list of all authenticated characters from characters.json.
    """
    characters = load_characters()
    # Return only public data
    public_chars = [{"char_id": c["character_id"], "name": c["name"]} for c in characters]
    return jsonify({
        'mode': 'sso',
        'characters': public_chars,
        'count': len(public_chars)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)