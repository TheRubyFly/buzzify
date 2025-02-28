from flask import Blueprint

# Créer un Blueprint pour organiser les routes
routes = Blueprint("routes", __name__)


@routes.route("/")
def index():
    return "Buzzer backend is running"
