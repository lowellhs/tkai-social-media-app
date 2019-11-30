#!/bin/sh

# Start Gunicorn processes
python manage.py makemigrations
python manage.py migrate
echo Starting Gunicorn.
exec gunicorn user.wsgi:application \
    --bind :8000 \
    --workers 3
