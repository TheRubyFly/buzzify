
import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
import { apiUrl } from "../config";
import { useNavigate } from "react-router-dom";


function Player() {
    const [buzzed, setBuzzed] = useState(null);
    const socket = io(apiUrl);
    const navigate = useNavigate();

    useEffect(() => {
        socket.on("buzzed", (data) => {
            console.log(apiUrl);
            setBuzzed(data.username);
        });

        socket.on("reset", () => {
            setBuzzed(null);
        });

        return () => socket.off();  // Nettoyage des événements
    }, []);

    const handleBuzz = () => {
        socket.emit("buzz", { username: "Joueur1" });
    };

    const handleReset = () => {
        socket.emit("reset");
    };

    return (
        <div>
            <div>
                 <button 
                 className="home-button" 
                 onClick={() => navigate("/")}>
                    <img src="https://cdn-icons-png.flaticon.com/512/25/25694.png" width="24" height="24"/>
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