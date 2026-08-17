# Payment Service

Платёжный сервис на FastAPI с PostgreSQL, RabbitMQ, Outbox Pattern и обработкой webhook.

## Стек

- Python 3.13
- FastAPI
- SQLAlchemy + PostgreSQL
- Alembic
- RabbitMQ
- FastStream
- Pydantic
- uv
- Docker / Docker Compose

---

## Структура проекта

```text
app/
├── api/                 # HTTP API
├── broker/              # RabbitMQ, topology, publishers
├── consumer/            # RabbitMQ consumer и обработка платежей
├── core/                # settings, database, dependencies
├── dto/                 # Pydantic schemas
├── models/              # SQLAlchemy models
└── services/
    └── outbox/          # Outbox worker

alembic/                 # миграции БД

docker-compose.yml       # полный запуск проекта
docker-compose.dev.yml   # PostgreSQL + RabbitMQ для локальной разработки
Dockerfile
```

---

## Переменные окружения

Для локального запуска используется файл `.env`:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=payment_service_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672

API_KEY=secret

WEBHOOK_TIMEOUT=10
WEBHOOK_MAX_RETRIES=3
```

> **Примечание:** Для запуска через Docker используется `.env.docker`, где хосты PostgreSQL и RabbitMQ заменяются на имена соответствующих сервисов (`postgres` и `rabbitmq`).

---

## Локальная разработка

### 1. Запустить PostgreSQL и RabbitMQ

```bash
docker compose -f docker-compose.dev.yml up -d
```

Проверить статус контейнеров:
```bash
docker compose -f docker-compose.dev.yml ps
```

- **RabbitMQ Management UI:** [http://localhost:15672](http://localhost:15672)
- **Логин / Пароль:** `guest` / `guest`

### 2. Применить миграции

```bash
uv run alembic upgrade head
```

### 3. Запустить API

```bash
uv run fastapi dev app/main.py
```

- **API:** [http://localhost:8000](http://localhost:8000)
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Запустить Consumer

В отдельном терминале:

```bash
uv run faststream run app.consumer.main:app
```

### 5. Запустить Outbox Worker

В ещё одном терминале:

```bash
uv run python -m app.services.outbox.main
```

---

### Архитектура взаимодействия компонентов

```text
FastAPI
   │
   ├── PostgreSQL
   │
   └── Outbox → RabbitMQ → Consumer
                         │
                         └── Payment processing → Webhook
```

---

## Запуск всего проекта через Docker

Для автоматического запуска всех сервисов (API, Consumer, Outbox Worker, PostgreSQL, RabbitMQ) и применения миграций:

```bash
docker compose up --build
```

### Доступные сервисы:
- **API:** [http://localhost:8000](http://localhost:8000)
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **RabbitMQ UI:** [http://localhost:15672](http://localhost:15672) (`guest` / `guest`)

---

## Остановка

Остановить проект (полный Docker):
```bash
docker compose down
```

Остановить окружение разработки (dev):
```bash
docker compose -f docker-compose.dev.yml down
```

Остановить dev-окружение и удалить все данные базы данных (volumes):
```bash
docker compose -f docker-compose.dev.yml down -v
```

---


## Тестирование Webhook

Для тестирования отправки webhook можно использовать сервис [webhook.site](https://webhook.site).

Полученный там уникальный URL укажите при создании платежа:

```json
{
  "amount": 100,
  "currency": "RUB",
  "webhook_url": "https://webhook.site/00000000-0000-0000-0000-000000000000"
}
```