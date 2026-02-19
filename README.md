Currency Tracker

Backend-приложение на Python с использованием PostgreSQL.
Проект полностью разворачивается через Docker Compose и не требует установки Python или PostgreSQL на хост-машину.

Быстрый запуск
1. Клонировать репозиторий
git clone <repo_url>
cd currency_tracker

2. Создать файл переменных окружения

Создать файл .env в корне проекта:

DB_HOST=db

DB_PORT=5432

DB_USER=postgres

DB_PASS=postgres

DB_NAME=test_task

3. Запустить проект
docker compose up --build

При первом запуске:

автоматически создаётся база данных test_task

поднимается PostgreSQL

запускается backend

Если ранее уже запускалось и база не создаётся — выполнить:

docker compose down -v
docker compose up --build

Подключение к базе внутри Docker

Backend подключается к БД по адресу:

postgresql://postgres:postgres@db:5432/test_task


Пример SQL-запроса с JOIN

SELECT 
    r.id AS request_id,
    r.timestamp,
    r.endpoint,
    r.status_code,
    resp.id AS response_id,
    resp.base_currency,
    resp.target_currency,
    resp.rate,
    resp.date AS exchange_date,
    resp.raw_data
FROM requests r
INNER JOIN responses resp ON r.id = resp.request_id
ORDER BY r.timestamp ASC


Запрос использует JOIN для связи таблицы снапшотов и таблицы кластеров по внешнему ключу cluster_id.

Остановка проекта
docker compose down


Удаление контейнеров и volume с БД:

docker compose down -v
