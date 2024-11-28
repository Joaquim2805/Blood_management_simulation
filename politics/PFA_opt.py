import itertools
import numpy as np

def PFA_optimization(complete_sim):
    # Paramètres initiaux
    t_low_fixed = [250] * 12  # \( \theta_{\text{low}} \) fixé à 250 pour chaque mois
    t_target_range = np.array([380,400, 600, 800])  # Plage pour \( \theta_{\text{target}} \)

    # Grouper les mois en 4 saisons
    # Hiver (Jan, Fev, Mar), Printemps (Avr, Mai, Juin), Été (Juil, Août, Sep), Automne (Oct, Nov, Déc)
    seasons = {
        "Hiver": [0, 1, 2],   # Janvier, Février, Mars
        "Printemps": [3, 4, 5],  # Avril, Mai, Juin
        "Été": [6, 7, 8],     # Juillet, Août, Septembre
        "Automne": [9, 10, 11]  # Octobre, Novembre, Décembre
    }

    # Itération sur les combinaisons possibles des valeurs de θ_target pour chaque saison
    best_cost = float('inf')
    best_params = None

    # Créer toutes les combinaisons possibles de valeurs pour chaque saison
    season_combinations = itertools.product(t_target_range, repeat=4)  # 4 saisons

    # Itération sur les combinaisons de valeurs de θ_target pour chaque saison
    for season_comb in season_combinations:
        # Assigner chaque valeur de θ_target à une saison spécifique
        t_target = [season_comb[0]] * 3 + [season_comb[1]] * 3 + [season_comb[2]] * 3 + [season_comb[3]] * 3

        if all(tl < tt for tl, tt in zip(t_low_fixed, t_target)):  # Vérifier les contraintes
            cost, stock_history, recourse_count,peremption= complete_sim(t_low_fixed, t_target)  # Simuler avec ces paramètres
            cost = np.sum(cost)
            if cost < best_cost:
                best_cost = cost
                best_params = (t_low_fixed, t_target)
                best_params = [list(map(int, group)) for group in best_params]
                print("Nouvelle solution optimale : ", best_params[1],best_cost)

    print("Meilleurs paramètres :", best_params)