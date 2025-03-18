"""
Module gérant les événements liés au buzzer via Flask-SocketIO.

- Gestion du temps de reset
- Événements de buzz et reset
"""

from flask import request
from flask_socketio import emit, rooms
from room import dic_rooms
from socketio_config import socketio


@socketio.on("set_reset_time")
def handle_set_reset_time(data):
    """Définit le temps avant la réinitialisation automatique du buzzer pour une room."""
    room_code = data["room"]
    dic_rooms[room_code]["reset_time"] = data["time"]
    emit("reset_time_updated", {"time": data["time"]}, room=room_code)


def reset_buzzer_after_delay(room_code, delay):
    """Réinitialise le buzzer après un délai spécifié."""
    socketio.sleep(delay)  # Non-bloquant, fonctionne bien avec event loop
    if room_code in dic_rooms:
        dic_rooms[room_code]["buzzed"] = "None"
        socketio.emit("reset", {}, room=room_code)


@socketio.on("buzz")
def handle_buzz(data):
    """Gère l'événement de buzz d'un joueur dans une room."""
    room_code = data["room"]
    username = data["username"]

    print(f"{username} a buzzé dans la room {room_code}")

    if room_code in dic_rooms:
        dic_rooms[room_code]["buzzed"] = username
        emit("buzzed", {"username": username}, room=room_code)

        # Démarrer le reset avec threading (au lieu de multiprocessing)
        reset_time = dic_rooms[room_code]["reset_time"]
        socketio.start_background_task(reset_buzzer_after_delay, room_code, reset_time)


@socketio.on("reset_host")
def handle_reset_host(data):
    """Permet à l'hôte de réinitialiser manuellement le buzzer."""
    room_code = data["room"]
    print(f"Reset manuel demandé par l'host pour la room {room_code}")

    if room_code in dic_rooms:
        dic_rooms[room_code]["buzzed"] = "None"
        socketio.emit("reset", {}, room=room_code)


@socketio.on("reset")
def handle_reset(data):
    """Permet au joueur qui a buzzé de réinitialiser le buzzer."""
    room_code = data["room"]
    username = data["username"]

    print(f"{username} essaye de reset le buzzer dans la room {room_code}")

    if room_code in dic_rooms and dic_rooms[room_code]["buzzed"] == username:
        dic_rooms[room_code]["buzzed"] = "None"
        emit("reset", room=room_code)
