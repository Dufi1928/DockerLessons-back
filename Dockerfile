# Utiliser une image Python officielle comme image de base
FROM python:3.8

# Définir le répertoire de travail dans le conteneur
WORKDIR /code

# Copier les fichiers de dépendances et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application dans le conteneur
COPY . .

# Exposer le port sur lequel Gunicorn va s'exécuter
EXPOSE 8000

# Utiliser Gunicorn pour lancer l'application
CMD ["uvicorn", "RevisionZenBackend.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
