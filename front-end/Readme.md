# Collaboration avec VIRBEL Théo Et Arthur Royer pour le projet
C'est la partie front-end de ce projet


# Tournoi Pokémon
Pour ce projet nous avons utilisé Flask qui est un framework de Python pour le web.

# Description

Vous allez développer un programme sur Python qui simule un tournoi entre 16 Pokémon choisis aléatoirement en utilisant les données de PokeAPI. Le programme doit effectuer des requêtes API pour récupérer les informations nécessaires, traiter les réponses, gérer les erreurs potentielles et automatiser le processus du tournoi jusqu'à la détermination du champion.

# Caractéristiques

- Récupère les données des Pokémon à partir de la PokeAPI.
- Simuler des combats entre Pokémon en se basant sur leurs statistiques d'attaque.
- Structure de tournoi avec 16 Pokémon, où les gagnants avancent à travers les tours.
- Affichage des résultats de chaque tour et du vainqueur final.


# Installation

Cloner le dépôt :

    ```bash
    git clone https://github.com/Theo-virbel/Pokemon.git
    ```

Créez et activez un environnement virtuel :

    ``bash
    python -m venv venv
    source venv/bin/activate # Pour Windows, utilisez : venv\Scripts\activate
    ```

Installez les dépendances nécessaires :

    ``bash
    pip install -r requirements.txt

Créez un fichier `requirements.txt` (si ce n'est pas déjà fait) en lançant la commande suivante :

    ``bash
    pip freeze > requirements.txt
    ```

## Exécuter l'application