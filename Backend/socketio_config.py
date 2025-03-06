"""
socketio_config.py

Ce module permet de générer la socket que nous allons utiliser dans l'application
"""

from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")  # Déclare le socket
