# Système de Vote Sécurisé en Django

Une application web de vote sécurisée construite avec Django, respectant les normes d'intégrité et d'anonymat des élections.

## 🚀 Fonctionnalités
- **Interface Utilisateur Responsive**: Classique, fluide, avec options *Mode Clair* et *Mode Sombre*.
- **Sécurité et Anonymat**: 
    - Séparation complète entre le votant (`Voter`) et le bulletin de vote (`Vote`).
    - Transactions de base de données atomiques pour garantir qu'aucun double vote n'est possible (si deux requêtes concourantes surviennent).
    - Protection CSRF et sécurisation des sessions.
- **Vérification d'Identité**: Authentification par pièce d'identité (NIN) combinée avec un code PIN secret.
- **Espace Administrateur**: Page d'administration Django entièrement configurée permettant un accès CRUD pour les Candidats et les Électeurs, mais une vue en *lecture seule* non modifiable pour les Votes.

## ⚙️ Prérequis
- Python 3.10 ou version ultérieure
- Git

## 🛠️ Installation et Lancement

1. **Cloner le repository et se placer dans le dossier**
```bash
git clone <URL_DU_REPO>
cd Vote
```

2. **Créer un environnement virtuel et l'activer**
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\\Scripts\\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Appliquer les migrations de la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Créer un super utilisateur (pour accéder à l'administration)**
```bash
python manage.py createsuperuser
# Suivez les instructions (nom d'utilisateur, email, mot de passe)
```

6. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

7. **Accès:**
- **Système de Vote (Client)** : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Administration** : [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 🧪 Tests
Le projet inclut des tests unitaires pour assurer la sécurité du processus.
Pour lancer les tests :
```bash
python manage.py test core
```

## 🔒 Normes de Vote Respectées
- **Un Homme, Un Vote** : Géré via de solides transactions atomiques et une vérification stricte des identifiants (has_voted).
- **Anonymat** : Aucun lien de traçabilité n'est conservé entre les modèles Vote et Voter dans la base de données après la soumission du formulaire.
- **Intégrité** : Le modèle Vote est restreint via l'Administration Django pour empêcher l'édition, l'ajout et la suppression manuels en backend par l'admin.
