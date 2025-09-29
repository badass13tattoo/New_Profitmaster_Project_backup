# Режимы работы приложения

## Локальный режим (по умолчанию)

Используется для тестирования с уже полученными данными из `local_data.json`.

### Запуск в локальном режиме:

```bash
python backend/app.py
```

или

```bash
set APP_MODE=local
python backend/app.py
```

### Доступные эндпоинты в локальном режиме:

- `GET /` - информация о режиме
- `GET /mode` - текущий режим работы
- `GET /characters` - список всех персонажей
- `GET /characters/<char_id>` - данные конкретного персонажа
- `GET /characters/<char_id>/refresh_token` - refresh token персонажа
- `GET /login` - информация о том, что авторизация отключена
- `GET /callback` - информация о том, что callback недоступен

## Production режим

Используется для реальной авторизации через EVE SSO.

### Запуск в production режиме:

```bash
set APP_MODE=production
python backend/app.py
```

### Требования для production режима:

- Файл `Application Settings.json` с реальными данными EVE SSO
- Настроенный callback URL для EVE SSO

### Доступные эндпоинты в production режиме:

- `GET /` - информация о режиме
- `GET /mode` - текущий режим работы
- `GET /login` - редирект на EVE SSO авторизацию
- `GET /callback` - обработка callback от EVE SSO

## Переключение режимов

### Для Windows:

```cmd
# Локальный режим
set APP_MODE=local
python backend/app.py

# Production режим
set APP_MODE=production
python backend/app.py
```

### Для Linux/Mac:

```bash
# Локальный режим
export APP_MODE=local
python backend/app.py

# Production режим
export APP_MODE=production
python backend/app.py
```

## Файлы конфигурации

### local_data.json (только для локального режима)

Содержит данные персонажей для тестирования:

```json
[
  {
    "name": "Character Name",
    "char_id": 123456789,
    "refresh_token": "your_refresh_token_here"
  }
]
```

### Application Settings.json (только для production режима)

Содержит настройки EVE SSO:

```json
{
  "clientId": "your_client_id",
  "clientSecret": "your_client_secret",
  "callbackUrl": "https://your-domain.com/callback",
  "scopes": ["publicData", "esi-skills.read_skills.v1"]
}
```

## Безопасность

- `local_data.json` и `Application Settings.json` исключены из Git
- Используйте `local_data.example.json` и `Application Settings.example.json` как шаблоны
- Никогда не коммитьте файлы с реальными токенами и секретами
