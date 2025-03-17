"""
app.py

Ce module initialise et configure le backend de Buzzify.

Il met en place un serveur Flask avec gestion des CORS et WebSockets via Flask-SocketIO.
"""

import os

from flask import Flask
from flask_cors import CORS
from route import \
    routes  # Import des routespip install flask flask-cors flask-socketio
from socketio_config import socketio  # Import de socketio

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
