# Utiliser l'image de base Python
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers locaux main.py et requirements.txt dans le répertoire du conteneur /app
COPY main.py requirements.txt /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 80 vers l'extérieur
EXPOSE 80

# Commande pour exécuter l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
