"""
buzz.py

Ce module permet de gérer toutes les actions liées au buzzer
"""

import threading
import time

# import room  # Gestion des rooms
from flask import request  # Flask,
from flask_socketio import emit, rooms  # SocketIO, join_room, leave_room,
from room import dic_rooms
from socketio_config import socketio


# Définir le temps de reset
@socketio.on("set_reset_time")
def handle_set_reset_time(data):
    """
    Permet de changer le temps maximal avant la réinitialisation du buzzer

    Args:
        data : un dictionnaire contenant
            -room : le code de la salle
            -time : le nouveau temps
    """
    room_code = data["room"]
    dic_rooms[room_code]["reset_time"] = data["time"]
    emit("reset_time_updated", {"time": data["time"]}, room=room_code)


# Réinitialisation automatique du buzzer après un délai
def reset_buzzer_after_delay(room_code, delay, socketio):
    """
    Permet de reset le buzzer automatiquement une fois le délai maximal dépassé

    Args:
        room_code : le code de la salle
        delay : le délai maximal
    """
    time.sleep(delay)  # Attendre le temps défini par l'utilisateur
    dic_rooms[room_code]["buzzed"] = "None"

    # Vérifier que socketio est bien initialisé avant d'émettre
    if socketio is not None:
        socketio.emit("reset", {}, room=room_code)
    else:
        print("SocketIO is not initialized!")


# Événement de buzz
@socketio.on("buzz")
def handle_buzz(data):
    """
    Permet à n'importe quel joueur de buzzer

    Args:
        data : un dictionnaire contenant
            -room : le code de la salle
            -username : le nom du joueur qui buzze
            -reset_time : le délai maximal avant reset
    """
    user_rooms = rooms(request.sid)  # Liste des rooms où est connecté cet utilisateur
    print(f"Utilisateur  est dans les rooms : {user_rooms}")
    room_code = data["room"]
    #   if room_code in dic_rooms:
    print(data["username"])
    dic_rooms[room_code]["buzzed"] = data["username"]
    emit("buzzed", {"username": data["username"]}, room=room_code)
    # Démarrer le compte à rebours pour réinitialiser le buzzer
    reset_time = dic_rooms[room_code]["reset_time"]
    threading.Thread(
        target=reset_buzzer_after_delay, args=(room_code, reset_time)
    ).start()


# Événement de réinitialisation du buzzer pour host
@socketio.on("reset_host")
def handle_reset_host(data):
    """
    Permet de gérer le reset dans le cas d'un joueur admin

    Args:
        data : un dictionnaire contenant
            -room : le code de la salle
    """
    room_code = data["room"]
    dic_rooms[room_code]["buzzed"] = "None"
    emit("reset", room=room_code)


# Événement de réinitialisation du buzzer
@socketio.on("reset")
def handle_reset(data):
    """
    Permet de gérer le reset dans le cas d'un joueur non admin

    data : un dictionnaire contenant
            -room : le code de la salle
            -usernam : le nom du joueur qui essaye de reset
    """
    print(data)
    room_code = data["room"]
    print(dic_rooms)
    print(dic_rooms[room_code])
    print(data["username"], " essaye de reset ", dic_rooms[room_code]["buzzed"])
    if data["username"] == (dic_rooms[room_code]["buzzed"] or False):
        dic_rooms[room_code]["buzzed"] = "None"
        emit("reset", room=room_code)
