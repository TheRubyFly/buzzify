import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
import { apiUrl } from "../config";

import { useNavigate } from "react-router-dom";


const socket = io(apiUrl);
function HostRoom() {
    const [buzzed, setBuzzed] = useState(null);
    const navigate = useNavigate();
    const [roomCode, setRoomCode] = useState(localStorage.getItem("room") || "");
    const [username, setUsername] = useState(localStorage.getItem("username") || "Joueur");
    const [resetTime, setResetTime] = useState(5);
    const [players, setPlayers] = useState([]);
    const [resetKey, setResetKey] = useState(0);


    const handleSetResetTime = (e) => {
        const time = parseInt(e.target.value, 10);
        if (!isNaN(time) && time > 0) {  // Vérifie que l'entrée est valide
            setResetTime(time);
            if (roomCode) {
                socket.emit("set_reset_time", { room: roomCode, time });
            }
        }
    };

    // Buzz
    const handleBuzz = () => {
        console.log("Quelqu'un a buzzé !")
        socket.emit("buzz", { username: username, room: roomCode });
        
    };

    const handleReset = () => {
        console.log("Réinitialisation buzzer")
        socket.emit("reset_host", {room: roomCode});
        
    };

    useEffect(() => {

        if (roomCode) {
            setTimeout(() => {
                console.log("📡 Envoi de 'join_room' avec", { room: roomCode, username });
                socket.emit("join_room", { room: roomCode, username });
            }, 500);
        }

        socket.on("room_joined", (data) => {
            console.log("📩 Réception de 'room_joined' avec", data);
            setPlayers(data.players);
        });

        setTimeout(() => {
            if (roomCode) {
                socket.emit("join_room", { room: roomCode, username });
            }
        }, 500);  // Attend 500 ms avant de rejoindre la room

        socket.on("buzzed", (data) => {
            setBuzzed(data.username);

        });

        socket.on("reset", () => {
            console.log("R buzzer");
            setBuzzed(null);
            setResetKey(prevKey => prevKey + 1);
        });

        socket.on("reset_time_updated", (data) => {
            setResetTime(data.time);
        });

        socket.on("room_joined", (data) => {
            console.log("📩 Réception de 'room_joined' :", data);
            setPlayers(data.players);     
        });

        return () => {
            socket.off("buzzed");
            socket.off("reset");
            socket.off("connect");
            socket.off("disconnect");
        };
    }, []);


    return (
        <div className="container">
            <div className="list-players">
                <h3>Liste des joueurs :</h3>
                {<ul>
                    {players.map((player, index) => (
                        <li key={index}>{player}</li>
                    ))}
                </ul>}
            </div>

            <div>
                 <button 
                 className="home-button" 
                 onClick={() => navigate("/")}>
                    <img src="https://banner2.cleanpng.com/20180411/ike/avfjoey57.webp" width="72" height="72"/>
                </button>
            </div>

            <div>
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
                    <button className = "bouton" onClick={handleReset}>Réinitialiser</button>
                </div>
                <div className="timer" >
                    <label>Temps de reset du buzzer (secondes) :</label>
                    <input 
                        
                        type="number"
                        value={resetTime}
                        onChange={handleSetResetTime}  // Met à jour le temps de reset
                        min="1"
                    />
                </div>
            </div>
        </div>
    );
}

export default HostRoom;