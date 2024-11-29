import numpy as np

def generate_instance(demand_type="low_variability", density="medium", trucks=6, capacity=500, alpha=1):
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

    # Définir les demandes
    if demand_type == "low_variability":
        demand = np.full(6, 200)  # Demande fixe
    elif demand_type == "high_variability":
        demand = np.random.randint(50, 500, size=6)  # Demande variable
    else:  # mixed
        demand = np.array([200, 300, 50, 400, 100, 500])

    # Définir l'instance
    instance = {
        "locations": locations,
        "demand": demand,
        "num_trucks": trucks,
        "truck_capacity": capacity,
        "truck_cost": alpha
    }
    return instance
