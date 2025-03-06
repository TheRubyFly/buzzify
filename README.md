# buzzify
Projet de conception logicielle de Gaspard Freydier et Camille Pellat


Pour récupérer les packages
pip install -r requirements.txt

Pour lancer l'application :
- Dans une console, entrer : 
    sudo docker pull gfreydier/buzzify:latest
    sudo docker run -p 8080:80 -p 5000:5000 gfreydier/buzzify
- se rendre sur localhost:8080/

A présent, vous pouvez créer une room, ou rejoindre une room préexistante. Si vous créer la room, vous aurez accès à la liste des joueurs dans la salle, et pourrez régler le délai maximal pour répondre le buzzer. Seul l'hôte et le joueur ayant buzzé peuvent réinitialiser le timer avant que le délai maximal soit terminé.

Il se peut que le serveur mette quelque temps à s'initialiser, nous vous recommandons d'attendre quelques secondes entre le moment où "npm run dev" est exécuté et le moment où vous créez une room.