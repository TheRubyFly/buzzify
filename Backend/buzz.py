import threading
import time

from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from room import rooms

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


# Définir le temps de reset
@socketio.on("set_reset_time")
def handle_set_reset_time(data):
    room_code = data["room"]
    if room_code in rooms:
        rooms[room_code]["reset_time"] = data["time"]
        emit("reset_time_updated", {"time": data["time"]}, room=room_code)


# Gérer le buzz
@socketio.on("buzz")
def handle_buzz(data):
    room_code = data["room"]
    if room_code in rooms and not rooms[room_code]["buzzed"]:
        rooms[room_code]["buzzed"] = True
        emit("buzzed", {"username": data["username"]}, room=room_code)

        # Démarrer le compte à rebours pour réinitialiser le buzzer
        reset_time = rooms[room_code]["reset_time"]
        threading.Thread(
            target=reset_buzzer_after_delay, args=(room_code, reset_time)
        ).start()


# Réinitialisation automatique du buzzer après un délai
def reset_buzzer_after_delay(room_code, delay):
    time.sleep(delay)  # Attendre le temps défini par l'utilisateur
    if room_code in rooms:
        rooms[room_code]["buzzed"] = False
        socketio.emit("buzzer_reset", {}, room=room_code)


# Réinitialisation manuelle du buzzer
@socketio.on("reset_buzzer")
def handle_reset_buzzer(data):
    room_code = data["room"]
    if room_code in rooms:
        rooms[room_code]["buzzed"] = False
        emit("buzzer_reset", {}, room=room_code)
