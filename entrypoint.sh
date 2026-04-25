#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until python -c "import psycopg2; psycopg2.connect(host='$DB_HOST', dbname='$DB_NAME', user='$DB_USER', password='$DB_PASSWORD')" 2>/dev/null; do
  sleep 1
done
echo "PostgreSQL ready."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn bus_conciertos.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
