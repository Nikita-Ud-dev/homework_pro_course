#!/bin/bash

set -e

echo "Запускаємо контейнер Django"

echo 'Чекаємо DB'
while ! nc -z course_db 5432; do
    sleep 1
done
echo "DB готова"

echo 'Чекаємо Redis'
while ! nc -z redis 6379; do
    sleep 1
done
echo "Redis готова"

if [[ "$1" == "web" || "$1" == "beat" ]]; then
    echo "Виконуємо міграції"
    python manage.py migrate --noinput

    echo "Збираємо статику"
    python manage.py collectstatic --noinput --clear
fi

case $1 in
    web)
        echo "Запускаємо сервер Django"
        exec python manage.py runserver 0.0.0.0:8000
        ;;
    worker)
        echo "Запускаємо Celery Worker"
        exec celery -A dj_app_mini worker --loglevel=info
        ;;
    beat)
        echo "Запускаємо Celery Beat"
        exec celery -A dj_app_mini beat --loglevel=info
        ;;
    *)
        echo "Запускаємо кастомну команду"
        exec "$@"
        ;;
esac

