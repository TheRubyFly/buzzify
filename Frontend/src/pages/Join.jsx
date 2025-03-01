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
        console.log(localStorage.getItem("room"))
        socket.emit("join_room", { room: code, username: pseudo });
    };

    function handleSubmit(e) {
        e.preventDefault();

        if (!code.trim() || !pseudo.trim()) {
            setError("Veuillez remplir tous les champs !");
            return;
        }

        setError("");
        console.log("Rejoindre la salle avec:", { code, pseudo });
        joinRoom();
        navigate("/room");
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
