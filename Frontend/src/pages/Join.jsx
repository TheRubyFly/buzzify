
import React, { useState, useEffect } from "react";


function MyForm() {
    // États pour stocker les valeurs des inputs
    const [code, setCode] = useState("");
    const [pseudo, setPseudo] = useState("");
    const [error, setError] = useState("");

    function handleSubmit(e) {
        e.preventDefault(); // Empêche le rechargement de la page

        // Vérification : les champs ne doivent pas être vides
        if (!code.trim() || !pseudo.trim()) {
            setError("Veuillez remplir tous les champs !");
            return; // Arrête l'exécution ici si un champ est vide
        }

        // Si tout est bon, on peut envoyer les données
        console.log("Rejoindre la salle avec:", { code, pseudo });
        setError(""); // Efface le message d'erreur
    }

    return (
        <form onSubmit={handleSubmit}>
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