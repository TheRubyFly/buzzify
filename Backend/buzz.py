import threading
import time

import room  # Gestion des rooms
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from room import dic_rooms
from socketio_config import socketio


# Définir le temps de reset
@socketio.on("set_reset_time")
def handle_set_reset_time(data):
    room_code = data["room"]
    dic_rooms[room_code]["reset_time"] = data["time"]
    emit("reset_time_updated", {"time": data["time"]}, room=room_code)


# Réinitialisation automatique du buzzer après un délai
def reset_buzzer_after_delay(room_code, delay):
    time.sleep(delay)  # Attendre le temps défini par l'utilisateur
    dic_rooms[room_code]["buzzed"] = False
    socketio.emit("reset", {}, room=room_code)


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
    reset_time = dic_rooms[room_code]["reset_time"]
    threading.Thread(
        target=reset_buzzer_after_delay, args=(room_code, reset_time)
    ).start()


# Événement de réinitialisation du buzzer
@socketio.on("reset")
def handle_reset(data):
    room_code = data["room"]
    dic_rooms[room_code]["buzzed"] = False
    emit("reset", room=room_code)
