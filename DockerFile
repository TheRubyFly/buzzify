FROM node:18-alpine

WORKDIR /app

# Définition de la variable d'environnement pour l'API au moment du build
ENV VITE_API_URL=http://localhost:8000
ENV VITE_ENVIRONNEMENT=local
# Installation des dépendances
COPY package.json package-lock.json ./
RUN npm install

# Copie du reste du code source
COPY . .
ENTRYPOINT ["npm", "run", "dev", "--", "--host=0.0.0.0"]