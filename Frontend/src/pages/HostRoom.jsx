
import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
import { apiUrl } from "../config";
import { useNavigate } from "react-router-dom";


function HostRoom() {
    const [buzzed, setBuzzed] = useState(null);
    const socket = io(apiUrl);
    const navigate = useNavigate();
    const [roomCode, setRoomCode] = useState(localStorage.getItem("room") || "");
    const [username, setUsername] = useState(localStorage.getItem("username") || "Joueur");
    const [resetTime, setResetTime] = useState(5);


    const handleSetResetTime = (e) => {
        const time = parseInt(e.target.value);
        setResetTime(time);
        if (roomCode) {
            socket.emit("set_reset_time", { room: roomCode, time });
        }
    };

    // Buzz
    const handleBuzz = () => {
        console.log("Quelqu'un a buzzé !")
        socket.emit("buzz", { username: username, room: roomCode });
        
    };

    const handleReset = () => {
        console.log("Réinitialisation buzzer")
        socket.emit("reset", {room: roomCode});
    };

    useEffect(() => {
        if (roomCode) {
            socket.emit("join_room", { room: roomCode, username });
        }

        socket.on("buzzed", (data) => {
            setBuzzed(data.username);

        });

        socket.on("reset", () => {
            setBuzzed(null);
        });

        socket.on("reset_time_updated", (data) => {
            setResetTime(data.time);
        });

        return () => socket.off();  // Nettoyage des événements
    }, []);


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
            <h2>ID : {roomCode}</h2>
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

export default HostRoom;