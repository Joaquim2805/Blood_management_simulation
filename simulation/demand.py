import numpy as np

def simulation_demand(size, month):
    """
    Simule la demande pour un hôpital en fonction de sa taille et du mois.
    
    Modifications :
    - Variation plus marquée entre les mois.
    - Introduction de pics aléatoires pour simuler des événements imprévus.
    
    Paramètres :
    ------------
    size : float
        Taille de l'hôpital (par exemple, population desservie ou capacité).
    month : int
        Mois (1 à 12). La demande est plus forte en hiver et plus faible en été.
    
    Retourne :
    ----------
    demande : float
        Demande simulée pour l'hôpital.
    """
    # Calcul du facteur saisonnier (maximal en hiver, minimal en été, symétrique)
    seasonal_factor = 1 + 0.9 * np.cos(2 * np.pi * (month - 1) / 12)

    # Ajout d'un pic aléatoire pour certains mois (par exemple, mois 2, 8, 11)
    peak_factor = 1.0
    if month in [2, 8, 11]:
        peak_factor += np.random.uniform(0.1, 0.3)  # Augmentation aléatoire de 10 à 30 %
    
    # Paramètres de base pour la distribution normale
    base_mean = 65   # Moyenne de base de la demande
    base_std = 15    # Écart type de base de la demande
    
    # Moyenne ajustée par la taille de l'hôpital, la saison et les pics
    mean = base_mean * size * seasonal_factor * peak_factor
    std = base_std * size  # L'écart type augmente avec la taille
    
    # Simulation de la demande
    demande = max(0, np.random.normal(mean, std))  # La demande ne peut pas être négative
    return demande
