import os
import threading
import time

from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, rooms
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
#import buzz  # Gestion du buzzer
import room  # Gestion des rooms

# Enregistrement des routes
app.register_blueprint(routes)

# Variable globale pour stocker l'utilisateur qui a buzzé



# Événement de buzz
@socketio.on("buzz")
def handle_buzz(data):
    user_rooms = rooms(request.sid)  # Liste des rooms où est connecté cet utilisateur
    print(f"Utilisateur  est dans les rooms : {user_rooms}")
    room_code = data["room"]
 #   if room_code in dic_rooms:
        # rooms[room_code]["buzzed"] = True
    emit("buzzed", {"username": data["username"]}, room=room_code)
        # Démarrer le compte à rebours pour réinitialiser le buzzer
        reset_time = rooms[room_code]["reset_time"]
        threading.Thread(
            target=reset_buzzer_after_delay, args=(room_code, reset_time)
        ).start()

# Événement de réinitialisation du buzzer
@socketio.on("reset")
def handle_reset(data):
    room_code = data["room"]
    rooms[room_code]["buzzed"] = False
    emit("reset", room=room_code)


# Lancement du serveur
if __name__ == "__main__":
    print("✅ Serveur Flask-SocketIO démarré avec succès !")
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
