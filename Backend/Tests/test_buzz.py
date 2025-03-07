"""
test_buzz.py

Ce module permet de tester les fonctions liées au buzzer via des tests unitaires
"""

import sys
import os

import unittest
from unittest.mock import patch
from flask import Flask
from flask_socketio import SocketIO
from buzz import (handle_buzz, handle_reset, handle_reset_host,
                  handle_set_reset_time, reset_buzzer_after_delay)
from room import dic_rooms


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Backend")))

class TestBuzzerFunctions(unittest.TestCase):
    """
    Test unitaires pour les fonctionnalités liées à buzz
    """
    def setUp(self):
        """
        Configuration de l'application et du SocketIO pour les tests
        
        Args:
            self : self
        """
        # Créer une instance Flask et lier SocketIO
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)

        # Ajout des routes et des événements pour les tests
        self.socketio.on_event("buzz", handle_buzz)

        # Créer un client de test SocketIO
        self.client = self.socketio.test_client(self.app)

    @patch("buzz.emit")
    @patch("buzz.rooms", return_value=["room1"])
    def test_handle_buzz(self, mock_rooms, mock_emit):
        """
        Test de handle_buzz

        Args:
            self : self
            mock_emit : objet de classe mock_emit        
        """
        dic_rooms["room1"] = {"buzzed": "None", "reset_time": 3}  # Initialisation

        # Émettre l'événement "buzz"
        self.client.emit("buzz", {"room": "room1", "username": "user1"})

        # # Vérification de l'état de la salle
        self.assertEqual(dic_rooms["room1"]["buzzed"], "user1")  # Vérifie l'état
        mock_emit.assert_called_with(
            "buzzed", {"username": "user1"}, room="room1"
        )  # Vérifie l'émission

    @patch("buzz.emit")
    def test_handle_set_reset_time(self, mock_emit):
        """
        Test de handle_set_reset_time

        Args:
            self : self
            mock_emit : objet de classe mock_emit        
        """
        dic_rooms["room1"] = {"reset_time": 0}
        handle_set_reset_time({"room": "room1", "time": 5})
        self.assertEqual(dic_rooms["room1"]["reset_time"], 5)
        mock_emit.assert_called_with("reset_time_updated", {"time": 5}, room="room1")

    @patch("buzz.socketio.emit")
    @patch("buzz.time.sleep", return_value=None)
    def test_reset_buzzer_after_delay(self, mock_sleep, mock_emit):
        """
        Test de reset_buzzer_after_delay

        Args:
            self : self
            mock_sleep : objet de classe mock_sleep
            mock_emit : objet de classe mock_emit        
        """
        dic_rooms["room1"] = {"buzzed": "user1"}
        reset_buzzer_after_delay("room1", 1)
        mock_sleep.assert_called_with(1)
        self.assertEqual(dic_rooms["room1"]["buzzed"], "None")
        mock_emit.assert_called_with("reset", {}, room="room1")

    @patch("buzz.emit")
    def test_handle_reset_host(self, mock_emit):
        """
        Test de handle_reset_host

        Args:
            self : self
            mock_emit : objet de classe mock_emit        
        """
        dic_rooms["room1"] = {"buzzed": "user1"}
        handle_reset_host({"room": "room1"})
        self.assertEqual(dic_rooms["room1"]["buzzed"], "None")
        mock_emit.assert_called_with("reset", room="room1")

    @patch("buzz.emit")
    def test_handle_reset(self, mock_emit):
        """
        Test de handle_reset

        Args:
            self : self
            mock_emit : objet de classe mock_emit        
        """
        dic_rooms["room1"] = {"buzzed": "user1"}
        handle_reset({"room": "room1", "username": "user1"})
        self.assertEqual(dic_rooms["room1"]["buzzed"], "None")
        mock_emit.assert_called_with("reset", room="room1")


if __name__ == "__main__":
    unittest.main()
