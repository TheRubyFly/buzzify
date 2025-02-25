import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";



function Host(){

    return(
        <div className="bruh">
        <h1>CODE</h1>
        <div>
            <button 
                className="bouton" 
                onClick={() => navigate("/Host")}
            >
                Créer une salle
            </button>
            <button >Rejoindre une salle</button>
        </div>
        </div>
    );

}

export default Home;