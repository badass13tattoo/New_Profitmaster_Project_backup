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

@app.route('/jobs')
def get_jobs():
    """Получить список всех работ для персонажей"""
    import random
    from datetime import datetime, timedelta
    
    jobs = []
    now = datetime.now()
    
    # Список реальных названий работ для EVE Online
    industry_jobs = [
        "Tritanium Mining", "Pyerite Extraction", "Mexallon Processing", 
        "Isogen Refining", "Nocxium Purification", "Zydrine Crystallization",
        "Megacyte Synthesis", "Morphite Compression", "Crimson Arkonor Mining",
        "Bistot Extraction", "Arkonor Processing", "Mercoxit Mining"
    ]
    
    research_jobs = [
        "Blueprint Research", "Material Efficiency Study", "Time Efficiency Analysis",
        "Invention Process", "Reverse Engineering", "Datacore Analysis",
        "Skill Training", "Blueprint Copying", "T3 Manufacturing Research",
        "Capital Ship Research", "Supercapital Research", "Titan Research"
    ]
    
    reaction_jobs = [
        "Simple Reaction", "Complex Reaction", "Advanced Reaction",
        "Catalyst Synthesis", "Intermediate Product", "Final Product",
        "Boosted Reaction", "Efficient Reaction", "Mass Reaction",
        "Specialized Reaction", "Rare Reaction", "Exotic Reaction"
    ]
    
    planetary_jobs = [
        "Planetary Command Center", "Extractor Head", "Basic Industry",
        "Advanced Industry", "High-Tech Industry", "Planetary Launch",
        "Resource Processing", "Planetary Defense", "Planetary Storage",
        "Planetary Power", "Planetary Link", "Planetary Customs"
    ]
    
    for char in local_characters:
        character_id = char['char_id']
        character_name = char['name']
        
        # Industry Jobs
        for i in range(char['industryJobs']['active']):
            start_time = now - timedelta(hours=random.randint(1, 24))
            duration_hours = random.randint(2, 8)
            end_time = start_time + timedelta(hours=duration_hours)
            
            jobs.append({
                'id': f'industry_{character_id}_{i}',
                'characterId': character_id,
                'characterName': character_name,
                'type': 'industry',
                'name': random.choice(industry_jobs),
                'startDate': start_time.isoformat(),
                'endDate': end_time.isoformat(),
                'status': 'active' if end_time > now else 'completed',
                'icon': '🏭',
                'location': f'Station {random.randint(1000, 9999)}',
                'blueprint': f'Blueprint {random.randint(100, 999)}',
                'runs': random.randint(1, 10),
                'progress': random.randint(0, 100) if end_time > now else 100
            })
        
        # Research Jobs
        for i in range(char['researchJobs']['active']):
            start_time = now - timedelta(hours=random.randint(1, 48))
            duration_hours = random.randint(12, 36)
            end_time = start_time + timedelta(hours=duration_hours)
            
            jobs.append({
                'id': f'research_{character_id}_{i}',
                'characterId': character_id,
                'characterName': character_name,
                'type': 'research',
                'name': random.choice(research_jobs),
                'startDate': start_time.isoformat(),
                'endDate': end_time.isoformat(),
                'status': 'active' if end_time > now else 'completed',
                'icon': '🔬',
                'location': f'Research Facility {random.randint(100, 999)}',
                'blueprint': f'Research Blueprint {random.randint(100, 999)}',
                'runs': random.randint(1, 5),
                'progress': random.randint(0, 100) if end_time > now else 100
            })
        
        # Reaction Jobs
        for i in range(char['reactionJobs']['active']):
            start_time = now - timedelta(hours=random.randint(1, 12))
            duration_hours = random.randint(1, 4)
            end_time = start_time + timedelta(hours=duration_hours)
            
            jobs.append({
                'id': f'reaction_{character_id}_{i}',
                'characterId': character_id,
                'characterName': character_name,
                'type': 'reaction',
                'name': random.choice(reaction_jobs),
                'startDate': start_time.isoformat(),
                'endDate': end_time.isoformat(),
                'status': 'active' if end_time > now else 'completed',
                'icon': '⚗️',
                'location': f'Reaction Facility {random.randint(100, 999)}',
                'blueprint': f'Reaction Formula {random.randint(100, 999)}',
                'runs': random.randint(1, 20),
                'progress': random.randint(0, 100) if end_time > now else 100
            })
        
        # Planetary Jobs
        for i in range(char['planetaryJobs']['active']):
            start_time = now - timedelta(minutes=random.randint(30, 360))
            duration_minutes = random.randint(30, 90)
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            jobs.append({
                'id': f'planetary_{character_id}_{i}',
                'characterId': character_id,
                'characterName': character_name,
                'type': 'planetary',
                'name': random.choice(planetary_jobs),
                'startDate': start_time.isoformat(),
                'endDate': end_time.isoformat(),
                'status': 'active' if end_time > now else 'completed',
                'icon': '🌍',
                'location': f'Planet {random.randint(1, 9)}',
                'blueprint': f'Planetary Blueprint {random.randint(100, 999)}',
                'runs': random.randint(1, 50),
                'progress': random.randint(0, 100) if end_time > now else 100
            })
    
    return jsonify({
        'mode': 'local',
        'jobs': jobs,
        'count': len(jobs)
    })

if __name__ == '__main__':
    print(f"Загружено персонажей из local_data.json: {len(local_characters)}")
    app.run(debug=True)