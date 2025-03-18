"""
test_room.py

Ce module permet de tester les fonctions liées aux salles via des tests unitaires
"""

import unittest
from unittest.mock import MagicMock, patch

from flask import Flask  # , request
from flask_socketio import SocketIO
from room import (dic_rooms, generate_room_code, handle_create_room,
                  handle_get_players, handle_join_room)

# from socketio_config import socketio


class TestRoomFunctions(unittest.TestCase):
    """
    Test unitaires pour les fonctionnalités liées aux salles
    """

    def setUp(self):
        """Configuration de l'application et du SocketIO pour les tests"""
        # Créer une instance Flask et lier SocketIO
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)

        # Ajout des routes et des événements pour les tests
        self.socketio.on_event("create_room", handle_create_room)
        self.socketio.on_event("join_room", handle_join_room)
        self.socketio.on_event("get_players", handle_get_players)

        # Créer un client de test SocketIO
        self.client = self.socketio.test_client(self.app)

    @patch("random.choices")
    def test_generate_room_code(self, mock_random_choices):
        """Test de la génération du code de salle"""
        mock_random_choices.return_value = ["A", "B", "C", "D", "E", "F"]
        room_code = generate_room_code()
        self.assertEqual(room_code, "ABCDEF")
        mock_random_choices.assert_called_once_with(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6
        )

    @patch("room.join_room")
    @patch("room.emit")
    def test_handle_create_room(self, mock_emit, mock_join_room):
        """Test de la création de salle"""
        data = {"username": "player1"}
        # Appeler l'événement de création de salle
        self.client.emit("create_room", data)
        # Attendre que la salle soit créée
        room_code = list(dic_rooms.keys())[1]
        mock_request = MagicMock()
        mock_request.sid = "fake_sid"  # ID de session simulé

        # # Vérifier que l'événement "room_created" a bien été émis avec room=None
        mock_emit.assert_called_once_with(
            "room_created", {"room": room_code}, room="fake_sid"
        )

    @patch("room.join_room")
    @patch("room.emit")
    def test_handle_join_room(self, mock_emit, mock_join_room):
        """Test de rejoindre une salle existante"""
        # Créer une salle manuellement pour tester l'ajout de joueur
        room_code = "ROOM123"
        dic_rooms[room_code] = {
            "players": ["player1"],
            "buzzed": None,
            "reset_time": 5,
        }

        data = {"username": "player2", "room": room_code}
        # Appeler l'événement pour rejoindre la salle
        self.client.emit("join_room", data)

        # Vérifier si le joueur a bien été ajouté à la liste des joueurs
        self.assertIn("player2", dic_rooms[room_code]["players"])

        # Vérifier que l'événement "room_joined" a bien été émis avec room=None
        mock_emit.assert_called_once_with(
            "room_joined",
            {"room": room_code, "players": ["player1", "player2"]},
            room=room_code,
        )

    @patch("room.emit")
    def test_handle_get_players(self, mock_emit):
        """Test pour récupérer la liste des joueurs d'une salle"""
        room_code = "ROOM123"
        dic_rooms[room_code] = {
            "players": ["player1", "player2"],
            "buzzed": None,
            "reset_time": 5,
        }

        data = {"room": room_code}
        mock_request = MagicMock()
        mock_request.sid = "fake_sid"  # ID de session simulé
        # Appeler l'événement pour obtenir la liste des joueurs
        self.client.emit("get_players", data)

        # Vérifier que la bonne liste des joueurs a été envoyée
        mock_emit.assert_called_once_with(
            "players_list", {"players": ["player1", "player2"]}, room="fake_sid"
        )

    @patch("room.emit")
    def test_handle_get_players_invalid_room(self, mock_emit):
        """Test pour récupérer la liste des joueurs si on est dans un salle invalide"""
        # Simuler une demande avec une salle inexistante
        data = {"room": "INVALIDROOM"}
        mock_request = MagicMock()
        mock_request.sid = "fake_sid"  # ID de session simulé

        # Simuler l'appel de l'événement
        self.client.emit("get_players", data)

        # Vérifier que l'événement d'erreur a bien été émis
        mock_emit.assert_called_once_with(
            "error", {"message": "Room inexistante"}, room="fake_sid"
        )


if __name__ == "__main__":
    unittest.main()