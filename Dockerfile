# ---- Build de l'application React
FROM node:18 AS frontend-build

WORKDIR /app

COPY Frontend/package*.json ./
RUN npm install

COPY Frontend ./
RUN npm run build

# ---- Build de l'API Python
FROM python:3.10 AS backend

WORKDIR /backend

# Installer les dépendances nécessaires pour la compilation (Gevent, Gunicorn, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY Backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY Backend ./
COPY Backend/ /backend/

# Ajouter Gunicorn (sans Gevent)
RUN pip install gunicorn --no-cache-dir || (echo "Installation de gunicorn échouée" && tail -n 100 /root/.pip/pip.log)

# =---- Création de l'image finale
FROM nginx:alpine

# Installer Python et pip dans l'image finale
RUN apk add --no-cache python3 python3-dev py3-pip

# Copier le backend Python depuis l'image backend
COPY --from=backend /backend /backend

# Créer un environnement virtuel pour Python
RUN python3 -m venv /backend/venv

# Activer l'environnement virtuel et installer les dépendances Python
RUN /backend/venv/bin/pip install --no-cache-dir -r /backend/requirements.txt

# Copier les fichiers frontend buildés vers Nginx
COPY --from=frontend-build /app/dist /usr/share/nginx/html

# Exposer les ports pour Nginx et le backend
EXPOSE 80 5000

ENV PYTHONPATH=/backend

# Lancer Nginx et l'application Flask via Gunicorn avec le worker sync
CMD ["sh", "-c", "nginx -g 'daemon off;' & /backend/venv/bin/gunicorn -k sync -b 0.0.0.0:5000 backend.app:app"]
