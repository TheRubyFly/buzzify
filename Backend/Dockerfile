# Utilisation de l'image officielle Python 3.10 comme base
FROM python:3.10

# Définition du répertoire de travail
WORKDIR /buzzify/Backend

# Copier tout le code du backend dans le conteneur
COPY . /buzzify/Backend/
ENV APP_TITLE=buzzify

# Installation des dépendances sans mise en cache pour un build plus léger
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Commande pour démarrer l'application
CMD ["python", "app.py"]