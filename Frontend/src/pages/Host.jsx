import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";



function Host(){

    // Créer une nouvelle room
    const createRoom = () => {
        socket.emit("create_room");
    };

    return(
        <div className="board">
        <h1>CODE</h1>
        <div>
            <button 
                className="bouton" 
                onClick={() => navigate("/Host")}
            >
                Créer une salle
            </button>
            <button 
                onClick={() => navigate("/Join")}
            >
                Rejoindre une salle
            </button>
        </div>
        </div>
    );
}

export default Host;