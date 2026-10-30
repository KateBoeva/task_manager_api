# Task Manager API

REST API для управления задачами, статусами и приоритетами.

## Стек технологий

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Testing**: pytest, pytest-asyncio
- **Server**: Uvicorn

## Установка

### Подготовка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd Task\ Manager\ API
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # На macOS/Linux
# или
venv\Scripts\activate  # На Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Установите переменные окружения:
```bash
cp service.env.example service.env
# Отредактируйте service.env с вашими параметрами БД
```

## Запуск

### Локальный запуск:
```bash
uvicorn app.main:app --reload
```

API будет доступен по адресу: `http://localhost:8000`
Документация Swagger: `http://localhost:8000/docs`

### С использованием Docker:
```bash
docker-compose up
```

## API Endpoints

### Tasks (Задачи)
- `GET /tasks` - список всех задач
- `GET /tasks/{task_id}` - получить задачу по ID
- `POST /tasks` - создать новую задачу

### Statuses (Статусы)
- `GET /statuses` - список всех статусов
- `GET /statuses/{status_id}` - получить статус по ID
- `POST /statuses` - создать новый статус
- `PUT /statuses/{status_id}` - обновить статус
- `DELETE /statuses/{status_id}` - удалить статус

### Priorities (Приоритеты)
- Планируется в будущих версиях

## Структура проекта

```
app/
├── main.py              # Основное приложение FastAPI
├── models.py            # Модели SQLAlchemy
├── schemas.py           # Pydantic схемы для валидации
├── database.py          # Конфигурация БД
├── settings.py          # Настройки приложения
├── repos/               # Слой репозиториев
│   ├── task_repo.py
│   └── status_repo.py
└── services/            # Бизнес-логика
    ├── task_service.py
    └── status_service.py

tests/
├── conftest.py          # Конфигурация pytest
└── test_status.py       # Тесты
```

## Тестирование

Запуск тестов:
```bash
pytest
```

Запуск с выводом покрытия:
```bash
pytest --cov=app
```

## TODO

- [ ] Использовать тестовую БД для тестов
- [ ] Добавить обработку ошибок (HTTPException)
- [ ] Добавить логирование
- [ ] Реализовать методы update и delete для Task
- [ ] Добавить интеграцию с AI
- [ ] Добавить аутентификацию

## Лицензия

MIT
