"""
Fichier principal de l'application Flask avec SocketIO.

- Initialise l'application Flask
- Configure Flask-SocketIO
- Enregistre les routes et démarre le serveur
"""

import os

import buzz  # Gestion du buzzer
import eventlet
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, rooms
from route import routes  # Import des routes
from socketio_config import socketio  # Import de socketio

eventlet.monkey_patch()

# Initialisation de l'application Flask
app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "clé-par-défaut")


# Ajout du support CORS (évite les erreurs de requêtes cross-origin)
CORS(app)

# Liaison de SocketIO avec l'application Flask
socketio.init_app(app)


# Enregistrement des routes
app.register_blueprint(routes)


# Lancement du serveur
if __name__ == "__main__":
    print("✅ Serveur Flask-SocketIO démarré avec succès !")
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
