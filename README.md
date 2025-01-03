# Application QCM en Python

Description

Une application interactive de Questionnaires à Choix Multiples (QCM) écrite en Python. Elle permet aux étudiants de répondre à des QCM et aux professeurs de gérer les résultats des étudiants. L'application est conçue pour être facile à utiliser, avec une interface en ligne de commande et des fonctionnalités distinctes pour les étudiants et les professeurs.

---

## 🚀 Fonctionnalités

### **Espace Étudiant**
- Inscription et connexion: Les étudiants peuvent créer un compte et se connecter pour accéder aux QCM.
- Réalisation de QCM par catégorie: Les étudiants peuvent choisir parmi différentes catégories de QCM et répondre aux questions.
- Affichage de l'historique des QCM réalisés: Les étudiants peuvent consulter leur historique de QCM, y compris les scores et les réponses fournies.
- Visualisation des réponses correctes et des scores: Après avoir terminé un QCM, les étudiants peuvent voir les réponses correctes et leur score.

### **Espace Professeur**
- Connexion au compte Professeur: Les professeurs peuvent se connecter à un compte dédié pour accéder aux fonctionnalités de gestion.
- Visualisation des résultats des étudiants: Les professeurs peuvent consulter les résultats de tous les étudiants, y compris les scores et les réponses.
- Ajout de nouveaux QCM : Les professeurs peuvent ajouter de nouveaux QCM avec des questions et des réponses, en choisissant entre des questions à choix unique ou multiple. 

---

## 🛠️ Prérequis

- **Python 3.x** : Assurez-vous d'avoir une version de Python installée sur votre système.
- **Bibliothèques utilisées** :  L'application utilise uniquement des modules standard de Python, donc aucune installation supplémentaire n'est nécessaire.

---

## 📦 Installation

1. Clonez le dépôt :
            git clone https://github.com/votre-utilisateur/votre-repo.git

2. Accédez au répertoire du projet :
            cd votre-repo

3. Exécutez l'application :
            python qcm_app.py


---
## ⚙️ Structure du Projet
   - qcm_app.py : Le fichier principal de l'application qui contient la logique de l'application.
   - qcms.json : Fichier JSON contenant les QCM disponibles, organisés par catégories et titres.      
   - users.json : Fichier JSON stockant les informations des utilisateurs (étudiants et professeurs).
   - history.json : Fichier JSON contenant l'historique des QCM réalisés par les étudiants.
   - scores.json : Fichier JSON stockant les scores cumulés des étudiants.
   - README.md : Fichier de documentation décrivant le projet.

--
## 📋 Utilisation
1. Espace Étudiant :

  - Inscrivez-vous ou connectez-vous.
  - Choisissez une catégorie et un QCM à réaliser.
  - Répondez aux questions et consultez votre score à la fin.
  - Consultez votre historique pour voir vos résultats précédents.

2. Espace Professeur :

  - Connectez-vous en tant que professeur en utilisant un compte dédié.
  - Consultez les résultats des étudiants.
  - Ajoutez de nouveaux QCM en suivant les instructions à l'écran.

---

## 📂 Exemples de fichiers JSON 
 - qcms.json : Contient les QCM disponibles, organisés par catégories et titres.

 - users.json : Stocke les informations des utilisateurs (étudiants et professeurs).

 - history.json : Contient l'historique des QCM réalisés par les étudiants.

 - scores.json : Stocke les scores cumulés des étudiants.

---

## 🖥️ Captures d'écran
