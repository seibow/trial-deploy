#!/bin/sh

if [ ! "$(ls -A /app/staticfiles 2>/dev/null)" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

exec "$@"