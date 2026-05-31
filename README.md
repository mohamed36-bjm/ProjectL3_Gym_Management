🚀 PowerFitness Management System
Ce projet est une application web dédiée à la gestion d'une salle de sport, développée avec Django. Elle permet une gestion centralisée des membres (athlètes, coachs) et un suivi administratif complet.

🎨 Design & Interface
Framework UI : Intégration du template Gentelella Alela! (basé sur Bootstrap) pour assurer une interface moderne et réactive.

Personnalisation : En plus du template, j'ai développé des fichiers HTML, CSS et JavaScript personnalisés afin d'adapter l'expérience utilisateur aux besoins spécifiques de "PowerFitness" (optimisation du style, interactions dynamiques et validation des formulaires).

Cohérence : L'interface a été uniformisée entre le Dashboard Manager et les espaces Profil/Compte pour une navigation fluide.

🔐 Système d'authentification
Le projet utilise deux points d'entrée sécurisés :

Espace Membres (Athlètes/Coachs) : Accessible via /login.

Espace Manager (Administration) : Accessible via /manager_login.

🛠️ Instructions pour les tests
Pour tester l'accès au tableau de bord Manager (Administration), vous pouvez utiliser le compte configuré :

Email : hichem@gmail.com

Mot de passe : hichemGalager

Note : Si vous souhaitez créer un nouveau compte administrateur, utilisez la commande suivante dans votre terminal :
python manage.py createsuperuser

⚙️ Choix techniques
Backend : Django (Python).

Sécurité : Utilisation de {% csrf_token %} pour la protection contre les failles CSRF et authentification sécurisée via le modèle User personnalisé.

Frontend : HTML5, CSS3, JavaScript et intégration du template Gentelella.

🚀 Installation
Cloner le dépôt : ```bash
git clone <URL_DU_PROJET>

Installer les dépendances : ```bash
pip install -r requirements.txt

Appliquer les migrations : ```bash
python manage.py migrate

Lancer le serveur : ```bash
python manage.py runserver


