
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";


function MyForm() {
    // États pour stocker les valeurs des inputs
    const [code, setCode] = useState("");
    const [pseudo, setPseudo] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const joinRoom = () => {
        socket.emit("join_room", { room: code, username: pseudo });
        localStorage.setItem("room", roomCode);  // Stocke la room
        localStorage.setItem("username", username);  // Stocke le pseudo
    };

    function handleSubmit(e) {
        e.preventDefault(); // Empêche le rechargement de la page

        // Vérification : les champs ne doivent pas être vides
        try {(code.trim() && pseudo.trim())}
        catch {
                    // Si tout est bon, on peut envoyer les données
        <joinRoom />
        console.log("Rejoindre la salle avec:", { code, pseudo });
        navigate("/room");
        setError(""); // Efface le message d'erreur

        }

        setError("Veuillez remplir tous les champs !");
        return; // Arrête l'exécution ici si un champ est vide
    
    }

    return (
        <form onSubmit={handleSubmit}>
            <div>
                 <button 
                 className="home-button" 
                 onClick={() => navigate("/")}>
                    <img src="https://banner2.cleanpng.com/20180411/ike/avfjoey57.webp" width="24" height="24"/>
                </button>
            </div>
            <div className="remplir">
                <label>
                    Code de la salle{" "}
                    <input
                        type="text"
                        value={code}
                        onChange={(e) => setCode(e.target.value)}
                    />
                </label>
            </div>
            <div className="remplir">
                <label>
                    Pseudo{" "}
                    <input
                        type="text"
                        value={pseudo}
                        onChange={(e) => setPseudo(e.target.value)}
                    />
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