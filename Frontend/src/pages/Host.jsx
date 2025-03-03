import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
import { apiUrl } from "../config";
import { useNavigate } from "react-router-dom";


function Host(){

    // Créer une nouvelle room
    const createRoom = () => {
        socket.emit("create_room", { username: pseudo });
        socket.once("room_created", (data) => {
            console.log("Rejoint la salle : ",data.room);
            localStorage.setItem("room", data.room);  // Stocke la room
            localStorage.setItem("username", pseudo);  // Stocke le pseudo
            setError(""); // Efface les erreurs précédentes
            navigate("/host_room"); // Navigue SEULEMENT si la room existe
        });
    };
    const navigate = useNavigate();
    const [code, setCode] = useState("");
    const [pseudo, setPseudo] = useState("");
    const [error, setError] = useState("");
    const socket = io(apiUrl);

    useEffect(() => {
        socket.on("room_created", (data) => {
            console.log("Rejoint la salle : ",data.room);
            localStorage.setItem("room", data.room);  // Stocke la room
            localStorage.setItem("username", pseudo);  // Stocke le pseudo
            setError(""); // Efface les erreurs précédentes
            navigate("/host_room"); // Navigue SEULEMENT si la room existe
        });
    });

    function handleSubmit(e) {
        e.preventDefault(); // Empêche le rechargement de la page

        // Vérification : les champs ne doivent pas être vides
        if (!pseudo.trim()) {
            setError("Veuillez remplir tous les champs !");
            return; // Arrête l'exécution ici si un champ est vide
        }

        // Si tout est bon, on peut envoyer les données
        console.log("Rejoindre la salle avec:", { pseudo });
        setError(""); // Efface le message d'erreur
        createRoom()
        // navigate("/host_room")
    }

    return(
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
                    Pseudo{" "}
                    <input
                        type="text"
                        value={pseudo}
                        onChange={(e) => setPseudo(e.target.value)}
                    />
                </label>
            </div>
            {error && <p style={{ color: "red" }}>{error}</p>}
        <div>   
            <button type="submit"
                className="bouton" 
            >
                Créer une salle
            </button>
        </div>
    </form>
    );
}

export default Host;