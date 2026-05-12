#!/bin/bash

set -e  # Останавливаем скрипт при любой ошибке

echo "🚀 Настройка проекта..."

# 1. Копируем .env если его нет
if [ ! -f .env ]; then
    echo "📝 Создаём .env из .env.example..."
    cp .env.example .env
else
    echo "✅ .env уже существует"
fi

# 2. Генерируем SECRET_KEY если он ещё не сгенерирован
if grep -q "your-secret-key-here" .env; then
    echo "🔑 Генерируем SECRET_KEY..."
    
    # Собираем образ (без запуска сервисов)
    echo "  ⏳ Сборка Docker образа api..."
    docker compose build api
    
    # Генерируем ключ через временный контейнер
    echo "  ⏳ Генерация секретного ключа..."
    SECRET_KEY=$(docker compose run --rm api python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 2>/dev/null | tail -n 1)
    
    # Проверяем, что ключ сгенерировался
    if [ -z "$SECRET_KEY" ]; then
        echo "❌ Ошибка: Не удалось сгенерировать SECRET_KEY"
        echo "   Попробуйте выполнить вручную:"
        echo "   docker compose run --rm api python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
        exit 1
    fi
    
    echo "  🔑 Сгенерирован ключ: $SECRET_KEY"
    
    # Заменяем в .env
    sed -i "s/your-secret-key-here/$SECRET_KEY/" .env
    
    echo "✅ SECRET_KEY добавлен в .env"
else
    echo "✅ SECRET_KEY уже настроен"
fi

# 3. Запускаем проект
echo "🐳 Запускаем Docker Compose..."
docker compose up --build