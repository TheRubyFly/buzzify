
import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
import { apiUrl } from "../config";
import { useNavigate } from "react-router-dom";


function HostRoom() {
    const [buzzed, setBuzzed] = useState(null);
    const socket = io(apiUrl);
    const navigate = useNavigate();
    const [room, setRoom] = useState("");
    const [roomCode, setRoomCode] = useState(localStorage.getItem("room") || "");
    const [username, setUsername] = useState(localStorage.getItem("username") || "Joueur");
    const [buzzerDisabled, setBuzzerDisabled] = useState(false);
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
        if (!buzzerDisabled) {
            socket.emit("buzz", { room: roomCode, username });
        }
    };

    const handleReset = () => {
        socket.emit("reset");
    };

    useEffect(() => {
        if (roomCode && username) {
            socket.emit("join_room", { room: roomCode, username });
        }

        socket.on("room_joined", (data) => {
            setRoomCode(data.room);
            setBuzzerDisabled(data.buzzed);
            setResetTime(data.reset_time);
        });

        socket.on("buzzed", (data) => {
            alert(`${data.username} a buzzé !`);
            setBuzzerDisabled(true);
        });

        socket.on("buzzer_reset", () => {
            setBuzzerDisabled(false);
        });

        socket.on("reset_time_updated", (data) => {
            setResetTime(data.time);
        });

        return () => {
            socket.off("room_created");
            socket.off("room_joined");
            socket.off("buzzed");
            socket.off("buzzer_reset");
            socket.off("reset_time_updated");
        };
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