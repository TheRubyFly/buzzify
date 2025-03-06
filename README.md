# buzzify
Projet de conception logicielle de Gaspard Freydier et Camille Pellat

***
## Objectifs

Cette application a pour but de créer des salles où vous et vos amis pourraient appuyer sur un buzzer, dans l'optique de vous accompagner lors de vos quizzs ou autres blindtests

***
## Organisation

L'application est composé de deux parties principales :
*Le frontend, construit avec React et Vite, c'est cette partie qui s'occupe de tout ce qui est affiché à l'écran, et de comment réagisse les éléments quand on interagit avec eux
*Le backend, codé sous Python, qui gère tout le côté serveur et les WebSockets

***
## Fonctionnement

Quand l'application est lancée, une WebSocket globale est créée. On peut ensuite recréer des rooms indépendantes à l'intérieur de la WebSocket. Le Frontend et le Backend échangeront alors ensuite grâce à des emits qui s'échangent à l'intérieur de la socket.

***
## Comment lancer l'application ?

* Dans une console, entrer : 
```
    sudo docker pull gfreydier/buzzify:latest
    sudo docker run -p 8080:80 -p 5000:5000 gfreydier/buzzify
```
* se rendre sur localhost:8080/

A présent, vous pouvez créer une room, ou rejoindre une room préexistante. Si vous créer la room, vous aurez accès à la liste des joueurs dans la salle, et pourrez régler le délai maximal pour répondre le buzzer. Seul l'hôte et le joueur ayant buzzé peuvent réinitialiser le timer avant que le délai maximal soit terminé.