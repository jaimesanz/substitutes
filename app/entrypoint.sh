#!/bin/sh
set -e

echo "Waiting for Postgres at ${POSTGRES_HOST}:${POSTGRES_PORT}..."
while ! python -c "import socket, os, sys
s = socket.socket()
try:
    s.connect((os.environ['POSTGRES_HOST'], int(os.environ['POSTGRES_PORT'])))
except Exception:
    sys.exit(1)
" 2>/dev/null; do
    sleep 1
done
echo "Postgres is up."

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Seeding reference data..."
python manage.py seed

# Create superuser if env vars provided and it doesn't exist yet.
if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Ensuring superuser exists..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
U = get_user_model()
email = '${DJANGO_SUPERUSER_EMAIL}'
if not U.objects.filter(email=email).exists():
    U.objects.create_superuser(email=email, password='${DJANGO_SUPERUSER_PASSWORD}')
    print('Superuser created:', email)
else:
    print('Superuser already exists:', email)
"
fi

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
