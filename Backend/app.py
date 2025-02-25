from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin pour le développement
socketio = SocketIO(app, cors_allowed_origins="*")

buzzed_user = None


@app.route("/")
def index():
    return "Buzzer backend is running"


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


if __name__ == "__main__":
    socketio.run(app, debug=True)
