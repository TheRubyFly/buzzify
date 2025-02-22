
import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";

const socket = io("http://localhost:5000");

function App() {
    const [buzzed, setBuzzed] = useState(null);

    useEffect(() => {
        socket.on("buzzed", (data) => {
            console.log("à buzzé");
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

export default App;
