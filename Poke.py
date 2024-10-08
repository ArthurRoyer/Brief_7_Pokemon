import requests
import random

# URL de base de l'API PokéAPI
BASE_URL = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"
BASE_URL_TYPE = "https://pokeapi.co/api/v2/type/"

# Cache pour les mouvements et leurs détails
move_cache = {}


# Fonction pour récupérer tous les Pokémon
def get_all_pokemon():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            data = response.json()
            return [(pokemon['name'], pokemon['url'].split('/')[-2]) for pokemon in data['results']]
        else:
            print(f"Erreur lors de la récupération des Pokémon : {response.status_code}")
            return []
    except Exception as e:
        print(f"Erreur : {e}")
        return []


# Fonction pour récupérer les détails d'un mouvement
def get_move_details(move_name):
    if move_name in move_cache:
        return move_cache[move_name]

    try:
        response = requests.get(f"https://pokeapi.co/api/v2/move/{move_name}")
        if response.status_code == 200:
            move_data = response.json()
            damage_class = move_data['damage_class']['name'] if move_data.get('damage_class') else 'N/A'
            move_details = {
                'name': move_data['name'],
                'power': move_data.get('power', 'N/A'),  # La puissance peut ne pas être disponible
                'type': move_data['type']['name'],
                'damage_class': damage_class.capitalize()
            }
            move_cache[move_name] = move_details  # Mettre en cache les détails du mouvement
            return move_details
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
                        'double_damage_to': {effect['name']: 2 for effect in
                                             effectiveness_data['damage_relations']['double_damage_to']},
                        'half_damage_to': {effect['name']: 0.5 for effect in
                                           effectiveness_data['damage_relations']['half_damage_to']},
                        'no_damage_to': {effect['name']: 0 for effect in
                                         effectiveness_data['damage_relations']['no_damage_to']},
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

    while True:  # Boucle jusqu'à ce qu'un Pokémon valide soit trouvé
        pokemon_name, pokemon_id = random.choice(pokemon_list)
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")

        if response.status_code == 200:
            data = response.json()
            stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
            types = [type_info['type']['name'] for type_info in data['types']]
            moves = [move['move']['name'] for move in data['moves']]

            if moves:
                selected_moves = random.sample(moves, min(4, len(moves)))
                moves_details = [get_move_details(move) for move in selected_moves]
                return {
                    'name': data['name'],
                    'types': types,
                    'stats': stats,
                    'moves': moves_details
                }
            else:
                print(f"{pokemon_name.capitalize()} n'a pas de moves. Récupération d'un autre Pokémon...")
        else:
            print(f"Erreur lors de la récupération du Pokémon avec ID {pokemon_id}")
            return None


# Fonction pour récupérer 16 Pokémon uniques avec leurs stats et moves
def get_unique_pokemons_with_details(pokemon_list, count=16):
    unique_pokemons = []
    while len(unique_pokemons) < count:
        random_pokemon = get_random_pokemon(pokemon_list)
        if random_pokemon and random_pokemon not in unique_pokemons:
            unique_pokemons.append(random_pokemon)

    return unique_pokemons


# Exemple d'utilisation
pokemon_list = get_all_pokemon()
unique_pokemons = get_unique_pokemons_with_details(pokemon_list, 16)

print("Liste des 16 Pokémon récupérés :")
for pokemon in unique_pokemons:
    print(
        f"\nPokémon : {pokemon['name'].capitalize()} (Types: {', '.join([poke_type.capitalize() for poke_type in pokemon['types']])})")
    print("Stats :")
    for stat_name, stat_value in pokemon['stats'].items():
        print(f"  - {stat_name.capitalize()}: {stat_value}")
    print(f"\nMoveset {pokemon['name'].capitalize()} :")
    for move in pokemon['moves']:
        print(
            f"  - {move['name'].capitalize()} (Type: {move['type'].capitalize()}, Puissance: {move['power']}, Classe de dégâts: {move['damage_class']})")
    print("-" * 50)


# Fonction pour calculer les dégâts
def calculate_damage(attacker, defender, move):
    base_power = move['power'] if isinstance(move['power'], int) else 0
    type_multiplier = 1

    attacker_types = attacker['types']
    defender_types = defender['types']

    # Appliquer la multiplication de type
    for attack_type in attacker_types:
        if attack_type in type_effectiveness:
            for defender_type in defender_types:  # Vérifiez chaque type défensif
                if defender_type in type_effectiveness[attack_type]['double_damage_to']:
                    type_multiplier *= 2
                elif defender_type in type_effectiveness[attack_type]['half_damage_to']:
                    type_multiplier *= 0.5
                elif defender_type in type_effectiveness[attack_type]['no_damage_to']:
                    return 0, 0  # Aucun dégâts infligé

    damage = base_power * type_multiplier
    return max(0, int(damage)), type_multiplier  # Ne pas permettre des dégâts négatifs


# Fonction pour simuler un combat entre deux Pokémon
def simulate_battle(pokemon1, pokemon2):
    stats1 = pokemon1['stats']
    stats2 = pokemon2['stats']

    hp1 = stats1.get('hp', 0)
    speed1 = stats1.get('speed', 0)

    hp2 = stats2.get('hp', 0)
    speed2 = stats2.get('speed', 0)

    if speed1 > speed2:
        first, second = pokemon1, pokemon2
        first_hp, second_hp = hp1, hp2
    else:
        first, second = pokemon2, pokemon1
        first_hp, second_hp = hp2, hp1

    print(
        f"{first['name'].capitalize()} attaque en premier avec une vitesse de {speed1 if first == pokemon1 else speed2}.")

    while first_hp > 0 and second_hp > 0:
        first_move = random.choice(first['moves'])
        damage, multiplier = calculate_damage(first, second, first_move)

        # Message d'efficacité de l'attaque
        if multiplier == 0:
            effectiveness_message = "Ça n'a aucun effet."
        elif multiplier == 0.5:
            effectiveness_message = "Ce n'est pas très efficace."
        elif multiplier == 2:
            effectiveness_message = "C'est super efficace."
        else:
            effectiveness_message = ""

        second_hp -= damage
        print(
            f"{first['name'].capitalize()} utilise {first_move['name'].capitalize()} et inflige {damage} points de dégâts à {second['name'].capitalize()}. {effectiveness_message} HP restants de {second['name'].capitalize()}: {max(second_hp, 0)}")

        if second_hp <= 0:
            print(f"{second['name'].capitalize()} est KO !")
            return first

        second_move = random.choice(second['moves'])
        damage, multiplier = calculate_damage(second, first, second_move)

        if multiplier == 0:
            effectiveness_message = "Ça n'a aucun effet."
        elif multiplier == 0.5:
            effectiveness_message = "Ce n'est pas très efficace."
        elif multiplier == 2:
            effectiveness_message = "C'est super efficace."
        else:
            effectiveness_message = ""

        first_hp -= damage
        print(
            f"{second['name'].capitalize()} utilise {second_move['name'].capitalize()} et inflige {damage} points de dégâts à {first['name'].capitalize()}. {effectiveness_message} HP restants de {first['name'].capitalize()}: {max(first_hp, 0)}")

        if first_hp <= 0:
            print(f"{first['name'].capitalize()} est KO !")
            return second

    return None


# Fonction pour organiser le tournoi
def run_tournament(pokemons):
    round_number = 1
    while len(pokemons) > 1:
        print(f"\n--- Tour {round_number} ---")
        winners = []
        for i in range(0, len(pokemons), 2):
            if i + 1 < len(pokemons):
                pokemon1 = pokemons[i]
                pokemon2 = pokemons[i + 1]
                print(f"{pokemon1['name'].capitalize()} vs {pokemon2['name'].capitalize()}")
                winner = simulate_battle(pokemon1, pokemon2)
                print(f"Vainqueur: {winner['name'].capitalize()}\n")
                winners.append(winner)
            else:
                print(f"{pokemons[i]['name'].capitalize()} passe au tour suivant sans combat.")
                winners.append(pokemons[i])

        pokemons = winners
        round_number += 1

    print(f"Vainqueur de la conférence de Verteresse : {pokemons[0]['name'].capitalize()}")


# Exemple d'utilisation pour exécuter le tournoi
type_effectiveness = get_type_effectiveness()
display_type_table(type_effectiveness)
run_tournament(unique_pokemons)
