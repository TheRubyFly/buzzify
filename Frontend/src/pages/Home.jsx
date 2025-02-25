import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";


const Home = () => {
    const navigate = useNavigate();
    
    return(
        <div className="board">
            <h1>Buzzify</h1>
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

export default Home;