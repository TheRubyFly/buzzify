import random
import string

from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from socketio_config import socketio

# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*")
print("accès à room.py réussi")
rooms = {"test": True}  # Dictionnaire pour stocker l'état de chaque room


# Générer un code de room aléatoire
def generate_room_code():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


# Gérer la création de room
@socketio.on("create_room")
def handle_create_room(data):
    room_code = generate_room_code()
    rooms[room_code] = {"buzzed": False}  # Initialiser la room avec un buzzer actif
    join_room(room_code)
    emit("room_created", {"room": room_code}, room=room_code)


# Gérer l'entrée dans une room
@socketio.on("join_room")
def handle_join_room(data):
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    room_code = data["room"]
    if room_code in rooms:
        join_room(room_code)
        emit(
            "room_joined",
            {"room": room_code},
            room=request.sid,
        )
    else:
        emit("error", {"message": "Room inexistante"}, room=request.sid)
