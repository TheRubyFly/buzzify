import os

from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from route import routes  # Import des routes
from socketio_config import socketio  # Import de socketio

# Initialisation de l'application Flask
app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "clé-par-défaut")


# Ajout du support CORS (évite les erreurs de requêtes cross-origin)
CORS(app)

# Liaison de SocketIO avec l'application Flask
socketio.init_app(app)

# Import des modules après l'initialisation pour éviter les imports circulaires
import buzz  # Gestion du buzzer
import room  # Gestion des rooms

# Enregistrement des routes
app.register_blueprint(routes)

# Variable globale pour stocker l'utilisateur qui a buzzé
buzzed_user = None


# Événement de buzz
@socketio.on("buzz")
def handle_buzz(data):
    global buzzed_user
    if buzzed_user is None:  # Si personne n'a encore buzzé
        buzzed_user = data["username"]
        emit("buzzed", {"username": buzzed_user}, broadcast=True)


# Événement de réinitialisation du buzzer
@socketio.on("reset")
def handle_reset():
    global buzzed_user
    buzzed_user = None
    emit("reset", broadcast=True)


# Lancement du serveur
if __name__ == "__main__":
    print("✅ Serveur Flask-SocketIO démarré avec succès !")
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
