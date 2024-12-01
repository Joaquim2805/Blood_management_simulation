import numpy as np

def generate_instance( density="medium", trucks=6, t_capacity=500, alpha=1):
    # Localisation des centres selon la densité
    if density == "low":
        locations = np.array([
            [0, 0],
            [20, 30],
            [50, 20],
            [10, 40],
            [60, 50],
            [30, 20]
        ])
    elif density == "high":
        locations = np.array([
            [0, 0],
            [2, 3],
            [3, 2],
            [1, 4],
            [4, 5],
            [3, 2]
        ])
    else:  # medium
        locations = np.array([
            [0, 0],
            [2, 3],
            [5, 2],
            [1, 4],
            [6, 5],
            [3, 2]
        ])



    return locations,len(locations),trucks,t_capacity,alpha
