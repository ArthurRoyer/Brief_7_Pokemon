import requests
import random

# URL de base de l'API PokéAPI
BASE_URL = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"


# Fonction pour récupérer tous les Pokémon
def get_all_pokemon():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            data = response.json()
            # Récupérer les Pokémon sous forme de liste (nom et ID)
            return [(pokemon['name'], pokemon['url'].split('/')[-2]) for pokemon in data['results']]
        else:
            print(f"Erreur lors de la récupération des Pokémon : {response.status_code}")
            return []
    except Exception as e:
        print(f"Erreur : {e}")
        return []


# Fonction pour récupérer les détails d'un mouvement
def get_move_details(move_name):
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/move/{move_name}")
        if response.status_code == 200:
            move_data = response.json()
            damage_class = move_data['damage_class']['name'] if move_data.get('damage_class') else 'N/A'
            return {
                'name': move_data['name'],
                'power': move_data.get('power', 'N/A'),  # La puissance peut ne pas être disponible
                'type': move_data['type']['name'],
                'damage_class': damage_class.capitalize()  # Ajout de la classe de dégâts
            }
        else:
            print(f"Erreur lors de la récupération du mouvement {move_name}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération du mouvement {move_name}: {e}")
        return None


# Fonction pour récupérer les données d'un Pokémon aléatoire
def get_random_pokemon(pokemon_list):
    if not pokemon_list:
        return None

    # Choisir un Pokémon aléatoire
    pokemon_name, pokemon_id = random.choice(pokemon_list)
    # Récupérer les détails du Pokémon
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")

    if response.status_code == 200:
        data = response.json()
        # Extraire les stats
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}

        # Extraire les mouvements
        moves = [move['move']['name'] for move in data['moves']]

        # Sélectionner 4 mouvements aléatoires
        selected_moves = random.sample(moves, min(4,
                                                  len(moves)))  # S'assurer de ne pas dépasser le nombre de mouvements disponibles

        # Récupérer les détails des mouvements sélectionnés
        moves_details = [get_move_details(move) for move in selected_moves]

        return {
            'name': data['name'],
            'stats': stats,
            'moves': moves_details  # Stocker les détails des mouvements
        }
    else:
        print(f"Erreur lors de la récupération du Pokémon avec ID {pokemon_id}")
        return None


# Fonction pour récupérer 16 Pokémon uniques avec leurs stats et mouvements
def get_unique_pokemons_with_details(pokemon_list, count=16):
    unique_pokemons = []  # Liste pour stocker les Pokémon avec leurs détails

    while len(unique_pokemons) < count:
        random_pokemon = get_random_pokemon(pokemon_list)
        if random_pokemon and random_pokemon not in unique_pokemons:
            unique_pokemons.append(random_pokemon)  # Ajouter le Pokémon avec ses détails

    return unique_pokemons


# Exemple d'utilisation
pokemon_list = get_all_pokemon()
unique_pokemons = get_unique_pokemons_with_details(pokemon_list, 16)

print("Liste des 16 Pokémon récupérés (sans doublon) :")
for pokemon in unique_pokemons:
    print(f"\nPokémon : {pokemon['name'].capitalize()}")
    print("Stats :")
    for stat_name, stat_value in pokemon['stats'].items():
        print(f"  - {stat_name.capitalize()}: {stat_value}")
    print("Mouvements sélectionnés :")
    for move in pokemon['moves']:
        print(
            f"  - {move['name'].capitalize()} (Type: {move['type'].capitalize()}, Puissance: {move['power']}, Classe de dégâts: {move['damage_class']})")
