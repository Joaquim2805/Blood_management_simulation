import numpy as np
import numpy as np

def simulation_disp(N, sizes, month):
    """
    Simule la disponibilité de sang pour N centres en fonction de leur taille et du mois.
    
    Paramètres :
    ------------
    N : int
        Nombre de centres de collecte.
    sizes : list ou array
        Liste des tailles des centres (par exemple, capacité ou classification).
    month : int
        Mois (1 à 12). Les variations saisonnières sont modélisées par une fonction continue.
    
    Retourne :
    ----------
    disponibilités : numpy array
        Disponibilités simulées pour chaque centre.
    """
    if len(sizes) != N:
        raise ValueError("La taille de 'sizes' doit correspondre au nombre de centres N.")
    
    # Calcul du facteur saisonnier continu (ajusté pour maximiser en été)
    seasonal_factor = 1 + 0.3 * np.cos(2 * np.pi * (month - 6) / 12)
    # Exemple :
    # - En été (mois 6, 7, 8), seasonal_factor ≈ 1.3
    # - En hiver (mois 12, 1, 2), seasonal_factor ≈ 0.7
    # - Printemps/automne : intermediate ≈ 1.0
    
    # Paramètres de base pour la distribution normale
    base_mean = 100  # Moyenne de base de la disponibilité
    base_std = 20    # Écart type de base de la disponibilité
    
    # Calcul des disponibilités
    disponibilités = []
    for size in sizes:
        # Moyenne ajustée par la taille du centre et la saison
        mean = base_mean * size * seasonal_factor
        std = base_std * size  # L'écart type augmente avec la taille
        disponibilités.append(int(max(0, np.random.normal(mean, std))))  # Disponibilité >= 0
    
    return np.array(disponibilités)

