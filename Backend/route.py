"""
room.py

Ce module permet de gérer les routes afin de relier app.py aux autres fichiers
"""

from flask import Blueprint

# Créer un Blueprint pour organiser les routes
routes = Blueprint("routes", __name__)


@routes.route("/")
def index():
    """
    Permet d'afficher l'état du serveur backend

    Ret:
        str    
    """
    return "Buzzer backend is running"
