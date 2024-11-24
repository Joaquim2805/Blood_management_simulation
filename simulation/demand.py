import numpy as np

def simulation_demand(size, month):
    """
    Simule la demande pour un hôpital en fonction de sa taille et du mois.
    
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
    # Calcul du facteur saisonnier (maximal en hiver et minimal en été)
    seasonal_factor = 1 + 0.3 * np.cos(2 * np.pi * (month - 12) / 12)
    # Exemple :
    # - En hiver (mois 12, 1, 2), seasonal_factor ≈ 1.3
    # - En été (mois 6, 7, 8), seasonal_factor ≈ 0.7
    # - Printemps/automne : intermediate ≈ 1.0
    
    # Paramètres de base pour la distribution normale
    base_mean = 80   # Moyenne de base de la demande
    base_std = 15    # Écart type de base de la demande
    
    # Moyenne ajustée par la taille de l'hôpital et la saison
    mean = base_mean * size * seasonal_factor
    std = base_std * size  # L'écart type augmente avec la taille
    
    # Simulation de la demande
    demande = max(0, np.random.normal(mean, std))  # La demande ne peut pas être négative
    return demande
