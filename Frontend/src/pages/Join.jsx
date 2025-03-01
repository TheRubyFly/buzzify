import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function MyForm() {
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
        e.preventDefault();

<<<<<<< HEAD
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
    
=======
        if (!code.trim() || !pseudo.trim()) {
            setError("Veuillez remplir tous les champs !");
            return;
        }

        setError("");
        console.log("Rejoindre la salle avec:", { code, pseudo });
        navigate("/Player");
>>>>>>> c4d1b16f1702c280774275628f7f6a517eeaa36a
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
