"""
Module gérant les rooms et leur état via Flask-SocketIO.

- Création et gestion des rooms
- Gestion des joueurs dans les rooms
"""

import random
import string

from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from socketio_config import socketio

print("✅ Accès à room.py réussi")

dic_rooms = {
    "test": {"reset_time": 5, "buzzed": "Personne"}
}  # Dictionnaire pour stocker l'état de chaque room


def generate_room_code():
    """Génère un code aléatoire pour une room."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


@socketio.on("create_room")
def handle_create_room(data):
    """Crée une nouvelle room et ajoute le créateur comme joueur."""
    room_code = generate_room_code()
    print(room_code)
    dic_rooms[room_code] = {
        "players": [data["username"]],
        "buzzed": None,
        "reset_time": 5,
    }
    join_room(room_code)
    emit("room_created", {"room": room_code}, room=request.sid)


@socketio.on("join_room")
def handle_join_room(data):
    """Ajoute un joueur à une room existante et envoie la mise à jour aux autres joueurs."""
    room_code = data["room"]
    print("Avant ajout :", dic_rooms[room_code]["players"])
    if room_code in dic_rooms:
        join_room(room_code)
        if data["username"] not in dic_rooms[room_code]["players"]:
            dic_rooms[room_code]["players"].append(data["username"])
        print("Après ajout :", dic_rooms[room_code]["players"])
        print(f"📡 Envoi de 'room_joined' à {request.sid}")
        emit(
            "room_joined",
            {"room": room_code, "players": dic_rooms[room_code]["players"]},
            room=room_code,
        )
        print("room_joined émis", dic_rooms[room_code]["players"])
    else:
        emit("error", {"message": "Room inexistante"}, room=request.sid)


@socketio.on("get_players")
def handle_get_players(data):
    """Envoie la liste des joueurs présents dans une room donnée."""
    room_code = data["room"]
    if room_code in dic_rooms:
        players = dic_rooms[room_code]["players"]
        print(f"🔹 Envoi de la liste des joueurs : {players}")
        emit("players_list", {"players": players}, room=request.sid)
    else:
        emit("error", {"message": "Room inexistante"}, room=request.sid)
