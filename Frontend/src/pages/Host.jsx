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
                    <img src="https://banner2.cleanpng.com/20180411/ike/avfjoey57.webp" width="72" height="72"/>
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