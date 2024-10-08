from flask import Flask, render_template, redirect, url_for, session
import requests
import random

# Création de l'application Flask
app = Flask(__name__)
# Clé secrète pour la gestion des sessions
app.secret_key = 'supersecretkey'

# URL de l'API Pokémon pour récupérer les données des Pokémon
BASE_URL = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"

# Fonction pour récupérer tous les Pokémon depuis l'API
def get_all_pokemon():
    try:
        # Faire une requête HTTP GET à l'API Pokémon
        response = requests.get(BASE_URL)
        if response.status_code == 200:  # Si la réponse est OK (200)
            data = response.json()  # Convertir la réponse JSON en dictionnaire
            # Retourner une liste de tuples (nom, ID) pour chaque Pokémon
            return [(pokemon['name'], pokemon['url'].split('/')[-2]) for pokemon in data['results']]
        else:
            # Si la réponse n'est pas 200, retourner une liste vide
            return []
    except Exception as e:
        # Si une erreur survient lors de la requête, l'afficher
        print(f"Erreur : {e}")
        return []

# Fonction pour récupérer un Pokémon aléatoire avec ses détails
def get_random_pokemon(pokemon_list):
    if not pokemon_list:
        return None

    # Choisir un Pokémon aléatoire dans la liste
    pokemon_name, pokemon_id = random.choice(pokemon_list)
    # Faire une requête à l'API pour récupérer les détails du Pokémon
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")

    if response.status_code == 200:  # Si la réponse est OK (200)
        data = response.json()  # Convertir la réponse JSON en dictionnaire
        # Extraire les statistiques du Pokémon (attaque, défense, etc.)
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        # Retourner les détails du Pokémon sous forme de dictionnaire
        return {
            'name': data['name'],
            'stats': stats,
            'id': pokemon_id,
            'sprite': data['sprites']['front_default']
        }
    else:
        # Si la réponse n'est pas 200, afficher une erreur et retourner None
        print(f"Erreur lors de la récupération du Pokémon avec ID {pokemon_id}")
        return None

# Fonction pour simuler un combat entre deux Pokémon
def simulate_battle(pokemon1, pokemon2):
    stats1 = pokemon1['stats']
    stats2 = pokemon2['stats']

    # Récupérer la statistique d'attaque des deux Pokémon
    attack1 = stats1.get('attack', 0)
    attack2 = stats2.get('attack', 0)

    # Comparer les attaques et retourner le gagnant
    if attack1 > attack2:
        return pokemon1
    elif attack2 > attack1:
        return pokemon2
    else:
        # Si les attaques sont égales, choisir un gagnant au hasard
        return random.choice([pokemon1, pokemon2])

# Fonction pour simuler un tournoi entre plusieurs Pokémon
def run_tournament(pokemons):
    while len(pokemons) > 1:
        round_winners = []
        # Parcourir la liste de Pokémon par paires
        for i in range(0, len(pokemons), 2):
            if i + 1 < len(pokemons):  # Si un deuxième Pokémon est présent pour affronter le premier
                pokemon1 = pokemons[i]
                pokemon2 = pokemons[i + 1]
                # Simuler le combat entre les deux Pokémon
                winner = simulate_battle(pokemon1, pokemon2)
                round_winners.append(winner)
            else:
                # Si un Pokémon n'a pas d'adversaire (cas des nombres impairs), il avance automatiquement
                round_winners.append(pokemons[i])
        # Mettre à jour la liste des Pokémon avec les gagnants de ce round
        pokemons = round_winners
    # Retourner le gagnant final (le seul Pokémon restant)
    return pokemons[0]

# Fonction pour récupérer un certain nombre de Pokémon uniques
def get_unique_pokemons_with_details(pokemon_list, count=16):
    unique_pokemons = []
    while len(unique_pokemons) < count:
        # Choisir un Pokémon aléatoire
        random_pokemon = get_random_pokemon(pokemon_list)
        # Vérifier si le Pokémon n'est pas déjà dans la liste des uniques
        if random_pokemon and random_pokemon not in unique_pokemons:
            unique_pokemons.append(random_pokemon)
    return unique_pokemons

# Route d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour la première manche du tournoi
@app.route('/round1')
def round1():
    pokemon_list = get_all_pokemon()  # Récupérer la liste de tous les Pokémon
    unique_pokemons = get_unique_pokemons_with_details(pokemon_list)  # Sélectionner 16 Pokémon uniques
    session['pokemons'] = unique_pokemons  # Conserver les Pokémon dans la session

    # Sélectionner les deux premiers Pokémon pour le premier combat
    first_battle = unique_pokemons[0:2]
    round1_winner = simulate_battle(first_battle[0], first_battle[1])

    # Sauvegarder le gagnant du round 1 dans la session
    session['round1_winner'] = round1_winner

    return render_template('round1.html', round1_result={'pokemon1': first_battle[0], 'pokemon2': first_battle[1], 'winner': round1_winner})

# Route pour le second round du tournoi
@app.route('/round2/<winner_id>')
def round2(winner_id):
    unique_pokemons = session.get('pokemons', [])  # Récupérer la liste des Pokémon de la session
    second_battle = unique_pokemons[2:4]  # Sélectionner les deux Pokémon pour le second combat
    round2_winner = simulate_battle(second_battle[0], second_battle[1])

    session['round2_winner'] = round2_winner  # Sauvegarder le gagnant du round 2 dans la session

    return render_template('round2.html', round2_result={'pokemon1': second_battle[0], 'pokemon2': second_battle[1], 'winner': round2_winner})

# Route pour le troisième round du tournoi
@app.route('/round3/<winner_id>')
def round3(winner_id):
    unique_pokemons = session.get('pokemons', [])  # Récupérer la liste des Pokémon de la session
    third_battle = unique_pokemons[4:6]  # Sélectionner les deux Pokémon pour le troisième combat
    round3_winner = simulate_battle(third_battle[0], third_battle[1])

    session['round3_winner'] = round3_winner  # Sauvegarder le gagnant du round 3 dans la session

    return render_template('round3.html', round3_result={'pokemon1': third_battle[0], 'pokemon2': third_battle[1], 'winner': round3_winner})

# Route pour démarrer le tournoi complet
@app.route('/tournament')
def tournament():
    pokemon_list = get_all_pokemon()  # Récupérer la liste des Pokémon
    unique_pokemons = get_unique_pokemons_with_details(pokemon_list)  # Sélectionner 16 Pokémon uniques
    session['pokemons'] = unique_pokemons  # Conserver les Pokémon dans la session

    # Lancer le tournoi complet et obtenir le gagnant final
    tournament_winner = run_tournament(unique_pokemons)
    
    # Récupérer les deux finalistes pour afficher le combat final
    final_battle = unique_pokemons[6:8]  # Les deux derniers Pokémon pour la finale
    round3_result = {
        'pokemon1': final_battle[0],
        'pokemon2': final_battle[1]
    }

    # Passer le gagnant du tournoi et les deux finalistes au template
    return render_template('tournament.html', winner=tournament_winner, round3_result=round3_result)

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
