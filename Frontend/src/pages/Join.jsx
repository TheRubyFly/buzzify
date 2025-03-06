import React, { useState, useEffect} from "react";
import { useNavigate } from "react-router-dom";
import { io } from "socket.io-client";
import { apiUrl } from "../config";

const socket = io(apiUrl);

function MyForm() {
    const [code, setCode] = useState("");
    const [pseudo, setPseudo] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        socket.on("room_joined", () => {
            console.log("Rejoint la salle !");
            setError(""); // Effacer les erreurs
            navigate("/room");
        });

        socket.on("error", (data) => {
            console.error("Erreur du serveur :", data.message);
            setError("Veuillez entrer un code valide");
        });

        return () => {
            socket.off("room_joined");
            socket.off("error");
        };
    }, [navigate]);

    const joinRoom = () => {
        localStorage.setItem("room", code);
        localStorage.setItem("username", pseudo);
        console.log("🔹 Tentative de connexion à", localStorage.getItem("room"));
            
        socket.emit("join_room", { room: code, username: pseudo });
    };


    function handleSubmit(e) {
        e.preventDefault();

        if (!code.trim() || !pseudo.trim()) {
            setError("Veuillez remplir tous les champs !");
            console.log(error)
            return;
        }

        joinRoom();
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
