## Требования к системе

- Docker Desktop 4.20+ (Windows/Mac) или Docker Engine 24+ (Linux)
- Docker Compose V2
- Git

## Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Topa18/endemics_api.git
cd endemics_api

# 2. Создать файл с переменными окружения
cp .env.example .env
# Отредактировать .env (указать пароли, ключи)

# 3. Собрать и запустить контейнеры
docker-compose up --build

# 4. В другом терминале выполнить миграции (если не выполнились автоматически)
docker-compose exec api python manage.py migrate

# 5. Создать суперпользователя (админа)
docker-compose exec api python manage.py createsuperuser

# Приложение доступно по адресу: http://localhost:8000
# Админ-панель: http://localhost:8000/admin
# API: http://localhost:8000/api/

# 6. Для остановки
docker-compose down

# 7. Для полной очистки (удалить данные БД)
docker-compose down -v