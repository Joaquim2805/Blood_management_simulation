import itertools
import numpy as np

def optimize_params_by_season(teta_low, teta_target, locations, N, K, Q, alpha, policy,complete_sim_with_peremption, discrete_values=None):
    """
    Trouve les meilleurs paramètres saisonniers pour minimiser le coût final
    en testant toutes les combinaisons possibles.

    Arguments:
    - teta_low, teta_target : seuils de la politique.
    - locations : positions des centres de collecte.
    - N : nombre de simulations à exécuter.
    - K : nombre de véhicules.
    - Q : capacité des véhicules.
    - alpha : facteur d'ajustement des coûts.
    - policy : politique à évaluer.
    - discrete_values : liste des valeurs discrètes possibles pour les paramètres.

    Retourne :
    - best_params : les meilleurs paramètres par saison (4 valeurs).
    - best_cost : le coût associé aux meilleurs paramètres.
    """
    if discrete_values is None:
        discrete_values = [-0.5, -0.25, 0, 0.25, 0.5]  # Par défaut, valeurs discrètes autorisées

    def evaluate_params(season_params):
        # Étend les paramètres saisonniers en une liste pour les 12 mois (3 mois par saison)
        full_params = np.repeat(season_params, 3)
        # Appelle la fonction de simulation et récupère le coût final
        final_cost, _, _, _ = complete_sim_with_peremption(
            teta_low, teta_target, locations, N, K, Q, alpha, policy, full_params, [0] * 12
        )
        return np.sum(final_cost)

    # Génère toutes les combinaisons possibles pour 4 saisons
    combinations = list(itertools.product(discrete_values, repeat=4))
    best_params = None
    best_cost = float('inf')

    # Parcourt toutes les combinaisons pour trouver la meilleure
    for i, season_params in enumerate(combinations):
        current_cost = evaluate_params(season_params)
        if current_cost < best_cost:
            best_cost = current_cost
            best_params = season_params

        # Affiche la progression
        print(f"Combination: {i+1}/{len(combinations)} | Params: {best_params} | Cost: {current_cost:.4f}", end="\r")

    print()  # Pour passer à la ligne après la progression
    return best_params, best_cost

# Exemple d'appel
best_params, best_cost = optimize_params_by_season(
    teta_low, teta_target, locations, N, K, Q, alpha, policy
)
print("Meilleurs paramètres par saison :", best_params)
print("Coût associé :", best_cost)
