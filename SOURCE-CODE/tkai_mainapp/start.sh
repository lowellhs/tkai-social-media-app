#!/bin/sh

# Start Gunicorn processes
python manage.py makemigrations
python manage.py migrate
echo Starting Gunicorn.
exec gunicorn mainapp.wsgi:application \
    --bind :8000 \
    --workers 3
