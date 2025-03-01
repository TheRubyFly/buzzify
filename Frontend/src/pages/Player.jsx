
import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
import { apiUrl } from "../config";
import { useNavigate } from "react-router-dom";

const socket = io(apiUrl);

function Player() {
    const [buzzed, setBuzzed] = useState(null);
    const [roomCode, setRoomCode] = useState(localStorage.getItem("room") || "");
    const [username, setUsername] = useState(localStorage.getItem("username") || "Joueur");
    const navigate = useNavigate();

    useEffect(() => {
        socket.on("buzzed", (data) => {
            setBuzzed(data.username);
        });

        socket.on("reset", () => {
            setBuzzed(null);
        });

        return () => socket.off();  // Nettoyage des événements
    }, []);

    const handleBuzz = () => {
        console.log("Quelqu'un a buzzé !")
        console.log(localStorage.getItem("username"))
        socket.emit("buzz", { username: username });
        
    };

    const handleReset = () => {
        console.log("Réinitialisation buzzer")
        socket.emit("reset");
    };

    return (
        <div>
            <div>
                 <button 
                 className="home-button" 
                 onClick={() => navigate("/")}>
                    <img src="https://banner2.cleanpng.com/20180411/ike/avfjoey57.webp" width="72" height="72"/>
                </button>
            </div>
            <h1>Buzzify</h1>
            <div>{buzzed ? <h2>{buzzed} a buzzé !</h2> : 
                <button 
                    className="buzzer" 
                    onClick={handleBuzz}>
                    <img src="https://www.espace-orthophonie.fr/1244519-large_default/buzzer.jpg" width="168" height="168"/>
                </button>}
            </div>
            <div>
                <button onClick={handleReset}>Réinitialiser</button>
            </div>
        </div>
    );
}

export default Player