"""
room.py

Ce module permet de gérer toutes les actions liées au salles
"""


import random
import string

from flask import request # Flask,
from flask_socketio import  emit, join_room #SocketIO, leave_room
from socketio_config import socketio

print("accès à room.py réussi")
dic_rooms = {
    "test": {"reset_time": 5, "buzzed": "Personne"}
}  # Dictionnaire pour stocker l'état de chaque room


# Générer un code de room aléatoire
def generate_room_code():
    """
    Crée un code aléatoire composé de 6 caractères compris entre les majuscules et les chiffres

    Ret:
        str (le code aléatoirement créé)
    """
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


# Gérer la création de room
@socketio.on("create_room")
def handle_create_room(data):
    """
    Permet de créer une salle

    Args :
        data : un dictionnaire contenant:
            -username : le nom du joueur qui crée la salle    
    """
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
    """
    Permet de rejoindre une salle

    Args :
        data : un dictionnaire contenant:
            -username : le nom du joueur qui rejoint la salle
            -room : le code de la salle   
    """
    room_code = data["room"]
    print("Avant ajout :", dic_rooms[room_code]["players"])
    if room_code in dic_rooms:
        join_room(room_code)
        if data["username"] not in dic_rooms[room_code]["players"]:
            dic_rooms[room_code]["players"].append(data["username"])
        print("Après ajout :", dic_rooms[room_code]["players"])
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
    """
    Permet de récupérer la liste des joueurs dans une salle

    Args :
        data : un dictionnaire contenant:
            -room : le code de la salle     
    """
    room_code = data["room"]
    if room_code in dic_rooms:
        players = dic_rooms[room_code]["players"]
        print(f"🔹 Envoi de la liste des joueurs : {players}")
        emit("players_list", {"players": players}, room=request.sid)
    else:
        emit("error", {"message": "Room inexistante"}, room=request.sid)
