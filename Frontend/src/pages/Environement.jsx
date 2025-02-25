const Environnement = () => {
    const environnement = import.meta.env.VITE_ENVIRONNEMENT || "local";
    const apiUrl = import.meta.env.VITE_API_URL || "localhost:8000";
    return (
      <div>
        <div>
          Environnement de déploiement : {environnement}, url d'api : {apiUrl}
        </div>
      </div>
    );
  };
  
  export default Environnement;