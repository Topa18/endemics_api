## Требования к системе

- Docker Desktop 4.20+ (Windows/Mac) или Docker Engine 24+ (Linux)
- Docker Compose V2
- Git

## Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Topa18/endemics_api.git
cd endemics_api

# Запустить автоматическую настройку и запуск контейнеров
chmod +x setup.sh
./setup.sh

# 5. Создать суперпользователя (админа)
docker compose exec api python manage.py createsuperuser

# Приложение доступно по адресу: http://localhost:8000
# Админ-панель: http://localhost:8000/admin
# API: http://localhost:8000/api/

# 6. Для остановки
docker compose down

# 7. Для полной очистки (удалить данные БД)
docker compose down -v