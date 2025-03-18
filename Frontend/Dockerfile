FROM node:18-alpine

WORKDIR /buzzify/Frontend

# Définition de la variable d'environnement pour l'API au moment du build
ENV VITE_API_URL=http://localhost:5000
ENV VITE_ENVIRONNEMENT=local

# Installation des dépendances
COPY package.json package-lock.json ./
RUN npm install

# Copie du reste du code source
COPY . /buzzify/Frontend/
ENTRYPOINT ["npm", "run", "dev", "--", "--host=0.0.0.0"]