import requests
import random

# URL de base de l'API PokéAPI
BASE_URL = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"
BASE_URL_TYPE = "https://pokeapi.co/api/v2/type/"


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


# Fonction pour récupérer les types et leurs effets
def get_type_effectiveness():
    type_effectiveness = {}
    try:
        response = requests.get("https://pokeapi.co/api/v2/type/")
        if response.status_code == 200:
            data = response.json()
            for type_info in data['results']:
                type_id = type_info['url'].split('/')[-2]
                effectiveness_response = requests.get(f"{BASE_URL_TYPE}{type_id}/")
                if effectiveness_response.status_code == 200:
                    effectiveness_data = effectiveness_response.json()
                    # Enregistrer les effets de type
                    type_effectiveness[type_info['name']] = {
                        'double_damage_to': {effect['name']: 2 for effect in effectiveness_data['damage_relations']['double_damage_to']},
                        'half_damage_to': {effect['name']: 0.5 for effect in effectiveness_data['damage_relations']['half_damage_to']},
                        'no_damage_to': {effect['name']: 0 for effect in effectiveness_data['damage_relations']['no_damage_to']},
                    }
    except Exception as e:
        print(f"Erreur lors de la récupération des types : {e}")

    return type_effectiveness


# Fonction pour afficher la table des types
def display_type_table(type_effectiveness):
    print("\nTable des Types de Pokémon et leurs effets :\n")
    for poke_type, effects in type_effectiveness.items():
        print(f"Type: {poke_type.capitalize()}")
        print(f"  - Dégâts doublés contre : {', '.join(effects['double_damage_to']).capitalize() or 'Aucun'}")
        print(f"  - Dégâts réduits de moitié contre : {', '.join(effects['half_damage_to']).capitalize() or 'Aucun'}")
        print(f"  - Aucun dégâts infligé contre : {', '.join(effects['no_damage_to']).capitalize() or 'Aucun'}")
        print("-" * 50)


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

print("Liste des 16 Pokémon récupérés :")
for pokemon in unique_pokemons:
    print(f"\nPokémon : {pokemon['name'].capitalize()}")
    print("Stats :")
    for stat_name, stat_value in pokemon['stats'].items():
        print(f"  - {stat_name.capitalize()}: {stat_value}")
    print(f"\nMoveset {pokemon['name'].capitalize()} :")
    for move in pokemon['moves']:
        print(
            f"  - {move['name'].capitalize()} (Type: {move['type'].capitalize()}, Puissance: {move['power']}, Classe de dégâts: {move['damage_class']})")
    print("-" * 50)



# Fonction pour simuler un combat entre deux Pokémon
def simulate_battle(pokemon1, pokemon2):
    # Extrait les stats des Pokémon
    stats1 = pokemon1['stats']
    stats2 = pokemon2['stats']

    # Exemple simple : comparaison de la stat d'attaque
    attack1 = stats1.get('attack', 0)
    attack2 = stats2.get('attack', 0)

    # Décider le vainqueur basé sur une simple comparaison d'attaque
    if attack1 > attack2:
        return pokemon1
    elif attack2 > attack1:
        return pokemon2
    else:
        # En cas d'égalité, choisir aléatoirement un vainqueur
        return random.choice([pokemon1, pokemon2])


# Fonction pour organiser le tournoi
def run_tournament(pokemons):
    round_number = 1
    while len(pokemons) > 1:
        print(f"\n--- Tour {round_number} ---")
        winners = []
        # Itérer à travers les Pokémon par paires
        for i in range(0, len(pokemons), 2):
            # Vérifier si on a assez de Pokémon pour un combat
            if i + 1 < len(pokemons):
                pokemon1 = pokemons[i]
                pokemon2 = pokemons[i + 1]
                print(f"{pokemon1['name'].capitalize()} vs {pokemon2['name'].capitalize()}")
                winner = simulate_battle(pokemon1, pokemon2)
                print(f"Vainqueur: {winner['name'].capitalize()}\n")
                winners.append(winner)  # Ajouter le vainqueur à la liste des gagnants

            else:
                # Si un nombre impair de Pokémon, le dernier Pokémon passe automatiquement au tour suivant
                print(f"{pokemons[i]['name'].capitalize()} passe au tour suivant sans combat.")
                winners.append(pokemons[i])

        # Mettre à jour les Pokémon pour le prochain tour
        pokemons = winners
        round_number += 1

    # Afficher le vainqueur final
    print(f"Vainqueur du tournoi: {pokemons[0]['name'].capitalize()}")


# Exemple d'utilisation pour exécuter le tournoi
type_effectiveness = get_type_effectiveness()
display_type_table(type_effectiveness)
run_tournament(unique_pokemons)










