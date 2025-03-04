import random
import string

from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from socketio_config import socketio

print("accès à room.py réussi")
dic_rooms = {
    "test": {"reset_time": 5}
}  # Dictionnaire pour stocker l'état de chaque room


# Générer un code de room aléatoire
def generate_room_code():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


# Gérer la création de room
@socketio.on("create_room")
def handle_create_room(data):

    room_code = generate_room_code()
    print(room_code)
    dic_rooms[room_code] = {
        "players": [data["username"]],
        "buzzed": None,
        "reset_time": 5,
    }  # Initialiser la room avec un buzzer actif
    join_room(room_code)
    emit("room_created", {"room": room_code}, room=request.sid)


# Gérer l'entrée dans une room
@socketio.on("join_room")
def handle_join_room(data):
    room_code = data["room"]
    if room_code in dic_rooms:
        join_room(room_code)
        # dic_rooms[room_code]["players"].append(data["username"])
        print(dic_rooms)
        emit(
            "room_joined",
            {"room": room_code},
            room=request.sid,
        )
        # emit("list_updated",{"list_players": dic_rooms[room_code]["players"]}, room=room_code)
    else:
        emit("error", {"message": "Room inexistante"}, room=request.sid)
