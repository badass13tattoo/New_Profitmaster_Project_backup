from flask import Flask, request, redirect, jsonify, session
from flask_cors import CORS
import requests
import json
import os
import base64

app = Flask(__name__)
CORS(app) # Разрешаем кросс-доменные запросы
app.secret_key = 'some_super_secret_key' # Секретный ключ для сессий

# Режим работы: 'local' для тестирования с local_data.json, 'production' для реальной авторизации
MODE = os.environ.get('APP_MODE', 'local')  # По умолчанию локальный режим

# Загружаем конфигурацию из Application Settings.json
def load_config():
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Application Settings.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise Exception("Файл Application Settings.json не найден")
    except json.JSONDecodeError:
        raise Exception("Ошибка парсинга Application Settings.json")

# Загружаем локальные данные для тестирования
def load_local_data():
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'local_data.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("Предупреждение: Файл local_data.json не найден. Локальный режим может не работать.")
        return []
    except json.JSONDecodeError:
        print("Ошибка парсинга local_data.json")
        return []

# Загружаем конфигурацию (только в production режиме)
if MODE == 'production':
    config = load_config()
    CLIENT_ID = config['clientId']
    SECRET_KEY = config['clientSecret']
    CALLBACK_URL = config['callbackUrl']
    SCOPES = ' '.join(config['scopes'])
else:
    # В локальном режиме используем заглушки
    CLIENT_ID = 'local_mode'
    SECRET_KEY = 'local_mode'
    CALLBACK_URL = 'http://localhost:5000/callback'
    SCOPES = 'local_mode'

# Загружаем локальные данные
local_characters = load_local_data()

# EVE SSO endpoints
AUTH_URL = 'https://login.eveonline.com/v2/oauth/authorize'
TOKEN_URL = 'https://login.eveonline.com/v2/oauth/token'

@app.route('/')
def home():
    mode_info = f" (режим: {MODE})"
    if MODE == 'local':
        return f"Привет! Это бэкенд в локальном режиме{mode_info}. Используются данные из local_data.json"
    else:
        return f"Привет! Это бэкенд в production режиме{mode_info}. Авторизируйся через фронтенд."

@app.route('/login')
def login():
    if MODE == 'local':
        return jsonify({
            'message': 'В локальном режиме авторизация отключена. Используются данные из local_data.json',
            'mode': 'local',
            'characters_available': len(local_characters)
        })
    
    # Создаем URL для авторизации с использованием скоупов из конфигурации
    auth_url = (f"{AUTH_URL}?response_type=code&redirect_uri={CALLBACK_URL}"
                f"&client_id={CLIENT_ID}&scope={SCOPES}")
    return redirect(auth_url)

@app.route('/callback')
def callback():
    if MODE == 'local':
        return jsonify({
            'message': 'В локальном режиме callback недоступен. Используйте /characters для получения данных персонажей.',
            'mode': 'local'
        })
    
    # Получаем код авторизации от EVE Online
    code = request.args.get('code')
    
    if not code:
        return jsonify({'error': 'Код авторизации не получен'}), 400
    
    # Создаем Basic Auth заголовок для EVE SSO
    credentials = f"{CLIENT_ID}:{SECRET_KEY}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    # Обмениваем код на токен
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'
    }
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
    }
    
    try:
        response = requests.post(TOKEN_URL, data=data, headers=headers)
        response.raise_for_status()  # Вызовет исключение для HTTP ошибок
        token_data = response.json()
        
        if 'access_token' in token_data:
            # Сохраняем токены в сессии
            session['access_token'] = token_data['access_token']
            if 'refresh_token' in token_data:
                session['refresh_token'] = token_data['refresh_token']
            # Здесь мы можем получить данные о персонаже
            return jsonify({'message': 'Авторизация прошла успешно!'})
        else:
            return jsonify({'error': 'Не удалось получить токен', 'details': token_data}), 400
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Ошибка при запросе токена: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Неожиданная ошибка: {str(e)}'}), 500

# Эндпоинты для работы с локальными данными
@app.route('/characters')
def get_characters():
    """Получить список всех персонажей из local_data.json"""
    if MODE == 'local':
        return jsonify({
            'mode': 'local',
            'characters': local_characters,
            'count': len(local_characters)
        })
    else:
        return jsonify({'error': 'Этот эндпоинт доступен только в локальном режиме'}), 400

@app.route('/characters/<int:char_id>')
def get_character(char_id):
    """Получить данные конкретного персонажа по ID"""
    if MODE == 'local':
        character = next((char for char in local_characters if char['char_id'] == char_id), None)
        if character:
            return jsonify({
                'mode': 'local',
                'character': character
            })
        else:
            return jsonify({'error': f'Персонаж с ID {char_id} не найден'}), 404
    else:
        return jsonify({'error': 'Этот эндпоинт доступен только в локальном режиме'}), 400

@app.route('/characters/<int:char_id>/refresh_token')
def get_refresh_token(char_id):
    """Получить refresh token для конкретного персонажа"""
    if MODE == 'local':
        character = next((char for char in local_characters if char['char_id'] == char_id), None)
        if character:
            return jsonify({
                'mode': 'local',
                'char_id': char_id,
                'name': character['name'],
                'refresh_token': character['refresh_token']
            })
        else:
            return jsonify({'error': f'Персонаж с ID {char_id} не найден'}), 404
    else:
        return jsonify({'error': 'Этот эндпоинт доступен только в локальном режиме'}), 400

@app.route('/mode')
def get_mode():
    """Получить текущий режим работы приложения"""
    return jsonify({
        'mode': MODE,
        'description': 'local' if MODE == 'local' else 'production',
        'characters_available': len(local_characters) if MODE == 'local' else 0
    })

if __name__ == '__main__':
    print(f"Запуск приложения в режиме: {MODE}")
    if MODE == 'local':
        print(f"Загружено персонажей из local_data.json: {len(local_characters)}")
    app.run(debug=True)