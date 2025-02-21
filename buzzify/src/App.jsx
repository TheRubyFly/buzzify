
import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";

const socket = io("http://localhost:5173");

function App() {
    const [buzzed, setBuzzed] = useState(null);

    useEffect(() => {
        socket.on("buzz", (data) => {
            console.log("buzzed");
            setBuzzed(data.username);
        });

        socket.on("reset", () => {
          console.log("reset");
            setBuzzed(null);
        });

        return () => socket.off();  // Nettoyage des événements
    }, []);

    const handleBuzz = () => {
      console.log("handleBuzz");
      console.log(buzzed);
        socket.emit("buzz", { username: "Joueur1" });
    };

    const handleReset = () => {
        socket.emit("reset");
    };

    return (
        <div>
            <h1>Buzzer App</h1>
            {buzzed ? <h2>{buzzed} a buzzé !</h2> : <div className="buzzer"><button onClick={handleBuzz}>Buzz</button></div>}
            <button onClick={handleReset}>Réinitialiser</button>
        </div>
    );
}

export default App;
