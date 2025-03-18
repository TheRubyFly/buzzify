"""
Module définissant les routes principales de l'application Flask.
"""

from flask import Blueprint

# Créer un Blueprint pour organiser les routes
routes = Blueprint("routes", __name__)


@routes.route("/")
def index():
    """Route principale affichant un message de statut."""
    return "Buzzer backend is running"
