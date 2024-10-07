import requests
import random
import time



# URL de base de l'API PokéAPI
BASE_URL = "https://pokeapi.co/api/v2/pokemon/"



# Fonction pour récupérer les données d'un Pokémon aléatoire
def get_random_pokemon():
    try:
        # Choisir un ID de Pokémon aléatoire entre 1 et 898 (nombre total de Pokémon dans la PokéAPI)
        pokemon_id = random.randint(1, 1302)
        response = requests.get(f"{BASE_URL}{pokemon_id}")

        if response.status_code == 200:
            data = response.json()
            # On extrait seulement les informations pertinentes
            return {
                'name': data['name'],
                'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
            }
        else:
            print(f"Erreur lors de la récupération du Pokémon avec ID {pokemon_id}")
            return None
    except Exception as e:
        print(f"Erreur : {e}")
        return None

