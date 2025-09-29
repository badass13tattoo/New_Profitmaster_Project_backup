from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Загружаем локальные данные для тестирования
def load_local_data():
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'local_data.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("Предупреждение: Файл local_data.json не найден.")
        return []
    except json.JSONDecodeError:
        print("Ошибка парсинга local_data.json")
        return []

# Загружаем локальные данные
local_characters = load_local_data()

@app.route('/')
def hello_world():
    return 'Hello, from the backend!'

@app.route('/characters')
def get_characters():
    """Получить список всех персонажей из local_data.json"""
    return jsonify({
        'mode': 'local',
        'characters': local_characters,
        'count': len(local_characters)
    })

if __name__ == '__main__':
    print(f"Загружено персонажей из local_data.json: {len(local_characters)}")
    app.run(debug=True)