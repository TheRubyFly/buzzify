import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";



function Host(){

    // Créer une nouvelle room
    const createRoom = () => {
        socket.emit("create_room");
    };
    const navigate = useNavigate();
    
    return(
        <div className="board">
        <div>
                 <button 
                 className="home-button" 
                 onClick={() => navigate("/")}>
                    <img src="https://cdn-icons-png.flaticon.com/512/25/25694.png" width="24" height="24"/>
                </button>
            </div>
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