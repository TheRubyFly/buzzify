from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from route import routes

# rooms = {"test" : ""}

app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin pour le développement
socketio = SocketIO(app, cors_allowed_origins="*")

print("accès à app.py réussi")

import buzz
import room

app.register_blueprint(routes)

buzzed_user = None


@socketio.on("buzz")
def handle_buzz(data):
    global buzzed_user
    if buzzed_user is None:
        buzzed_user = data["username"]
        emit("buzzed", {"username": buzzed_user}, broadcast=True)


@socketio.on("reset")
def handle_reset():
    global buzzed_user
    buzzed_user = None
    emit("reset", broadcast=True)


# # Gérer l'entrée dans une room
# @socketio.on("join_room")
# def handle_join_room(data):
#     print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
#     room_code = data["room"]
#     if room_code in rooms.keys():
#         join_room(room_code)
#         emit(
#             "room_joined",
#             {"room": room_code},
#             room=request.sid,
#         )
#     else:
#         emit("error", {"message": "Room inexistante"}, room=request.sid)

if __name__ == "__main__":
    socketio.run(app, debug=True)
