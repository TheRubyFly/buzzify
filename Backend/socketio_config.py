"""
Configuration de Flask-SocketIO pour gérer les WebSockets.
"""

from flask_socketio import SocketIO

# Déclare le socket avec CORS autorisé pour toutes les origines
socketio = SocketIO(cors_allowed_origins="*")
