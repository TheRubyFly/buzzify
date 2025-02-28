
import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
import { apiUrl } from "../config";

function Player() {
    const [buzzed, setBuzzed] = useState(null);
    const socket = io(apiUrl);

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
        <div className="bruh">
            <h1>Buzzify</h1>
            <div>{buzzed ? <h2>{buzzed} a buzzé !</h2> : <button className="buzzer" onClick={handleBuzz}>Buzz</button>}</div>
            <div><button onClick={handleReset}>Réinitialiser</button></div>
        </div>
    );
}

export default Player