#!/bin/sh

# Attendre que la base de données soit prête
while ! nc -z db 5432; do
  sleep 0.1
done

# Appliquer les migrations Django
python manage.py migrate --noinput

# Démarrer Gunicorn avec l'application Django
gunicorn --workers=3 --bind=0.0.0.0:8080 myproject.wsgi:application
