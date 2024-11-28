import numpy as np


def PFA(stock, month, disp,teta_low,teta_target):
    """
    Politique de décision PFA avec seuils et cibles définis dans la fonction.

    Paramètres :
    - stock : quantité actuelle de sang en stock
    - month : mois courant (1 à 12)
    - disp : disponibilités de sang dans les centres

    Retourne :
    - Quantité de sang à commander
    """
    # Définir les seuils (\(\theta_{\text{low}}\)) et les cibles (\(\theta_{\text{target}}\)) pour chaque mois
    #teta_low = [300, 300, 250, 250, 250, 200, 250, 250, 250, 250, 300, 350]  # Seuils par mois
    #teta_target = [680, 650, 550, 500, 480, 450, 480, 500, 500, 550, 650, 680]  # Cibles par mois

    # Récupérer les valeurs pour le mois donné
    t_low = teta_low[month - 1]
    t_target = teta_target[month - 1]

    # Calculer la quantité à commander
    if stock <= t_low and t_target - stock <= np.sum(disp):
        return t_target - stock
    elif stock <= t_low and t_target - stock >= np.sum(disp):
        return np.sum(disp)
    else:
        return 0

