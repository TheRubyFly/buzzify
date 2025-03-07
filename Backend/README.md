
Définir dans le .env la clé de scriptage de l'application
SECRET_KEY="Clé-que-vous-choississez"

Pour lancer les tests faire:
cd Backend
python3 -m unittest discover Tests


Les test qui ne fonctionnent pas échouent car je n'ai pas été capable de répliquer un request.sid dans les tests, mais ils sembleraient fonctionner sans ce problème.
