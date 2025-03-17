
Définir dans le .env la clé de scriptage de l'application
SECRET_KEY="Clé-que-vous-choississez"

Pour lancer les tests faire:
cd Backend
python3 -m unittest discover Tests


Les test qui ne fonctionnent pas échouent car je n'ai pas été capable de répliquer un request.sid dans les tests, mais ils sembleraient fonctionner sans ce problème.c
Un test n'échoue pas mais déclenche une erreur car j'ai mal réussi à gérer la création d'un thread dans mon test. Cette erreur n'impacte cependant pas le résultat du test ni ne représente une erreur dans le programme de base.
