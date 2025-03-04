import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { io } from "socket.io-client";
import { apiUrl } from "../config";

const socket = io(apiUrl);

function MyForm() {
    const [code, setCode] = useState("");
    const [pseudo, setPseudo] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const joinRoom = () => {
        localStorage.setItem("room", code);  // Stocke la room
        localStorage.setItem("username", pseudo);  // Stocke le pseudo
        console.log("tentative de connexion à", localStorage.getItem("room"))
        socket.emit("join_room", { room: code, username: pseudo });
    
        socket.once("room_joined", () => {
            console.log("Rejoint la salle :");
            setError(""); // Efface les erreurs précédentes
            getPlayers()
            navigate("/room"); // Navigue SEULEMENT si la room existe
        });
    
        // Écoute l'événement "error" pour gérer les erreurs
        socket.once("error", (data) => {
            console.error("Erreur du serveur :", data.message);
            setError("Veuillez entrer un code valide"); // Affiche l'erreur
            return;
        });
    
        // Envoie la requête au serveur
        socket.emit("join_room", { room: code, username: pseudo });
    };

    function handleSubmit(e) {
        e.preventDefault();

        if (!code.trim() || !pseudo.trim()) {
            setError("Veuillez remplir tous les champs !");
            console.log(error)
            return;
        }

        joinRoom();
    }

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <button 
                    className="home-button" 
                    onClick={() => navigate("/")}>
                    <img src="https://banner2.cleanpng.com/20180411/ike/avfjoey57.webp" width="72" height="72"/>
                </button>
            </div>
            <div className="remplir">
                <label>
                    Code de la salle{" "}
                    <input type="text" value={code} onChange={(e) => setCode(e.target.value)} />
                </label>
            </div>
            <div className="remplir">
                <label>
                    Pseudo{" "}
                    <input type="text" value={pseudo} onChange={(e) => setPseudo(e.target.value)} />
                </label>
            </div>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <div>
                <button type="submit">Confirmer</button>
            </div>
        </form>
    );
}

export default MyForm;
