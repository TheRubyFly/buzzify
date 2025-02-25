import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";



function Home(){
    const Home = () => {
        const navigate = useNavigate();
    }
    return(
        <div className="bruh">
        <h1>Buzzify</h1>
        <div>
            <button 
                className="bouton" 
                onClick={() => navigate("/about")}
            >
                Créer une salle
            </button>
            <button >Rejoindre une salle</button>
        </div>
        </div>
    );

}

export default Home;