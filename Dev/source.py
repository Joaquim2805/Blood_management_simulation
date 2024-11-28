import gurobipy as gp
from gurobipy import GRB
import numpy as np
import matplotlib.pyplot as plt


def recolte_sang(N,K,Q,S_min,alpha,locations,dispo,debug):
    
    distances = np.linalg.norm(locations[:, np.newaxis] - locations[np.newaxis, :], axis=2)

    model = gp.Model("Vehicle Routing Problem with Recourse")

    # Variables de décision
    x = model.addVars(N, N, K, vtype=GRB.BINARY, name="x")  # Si le camion k utilise l'arête (i, j)
    q = model.addVars(N, K, vtype=GRB.CONTINUOUS, name="q")  # Quantité collectée au centre i par camion k
    z = model.addVars(K, vtype=GRB.BINARY, name="z")  # Si le camion k est utilisé
    u = model.addVars(N, K, vtype=GRB.CONTINUOUS, lb=0, name="u")


    # Fonction objectif
    model.setObjective(
        gp.quicksum(distances[i, j] * x[i, j, k] for i in range(N) for j in range(N) for k in range(K)) +
        alpha * gp.quicksum(z[k] for k in range(K)),
        GRB.MINIMIZE
    )

    # Contrainte : satisfaire la demande minimale de sang
    model.addConstr(gp.quicksum(q[i, k] for i in range(1, N) for k in range(K)) >= S_min, "min_stock")


    for k in range(K):
        for i in range(1, N):
            for j in range(1, N):
                if i != j:
                    model.addConstr(u[i, k] - u[j, k] + N * x[i, j, k] <= N - 1, f"subtour_elimination_{i}_{j}_{k}")


    # Contrainte : capacité des camions
    for k in range(K):
        model.addConstr(gp.quicksum(q[i, k] for i in range(N)) <= Q * z[k], f"capacity_{k}")

    # Contrainte : collecte possible uniquement si visite
    for i in range(1, N):
        for k in range(K):
            model.addConstr(q[i, k] <= dispo[i] * gp.quicksum(x[i, j, k] for j in range(N)), f"visit_collect_{i}_{k}")

    # Contrainte : flux entrant et sortant équilibré pour chaque centre
    for i in range(1, N):
        for k in range(K):
            model.addConstr(
                gp.quicksum(x[i, j, k] for j in range(N)) == gp.quicksum(x[j, i, k] for j in range(N)),
                f"flow_{i}_{k}"
            )

    # Limitation de l'activation des camions : les trajets sont possibles uniquement si le camion est activé
    for k in range(K):
        for i in range(N):
            model.addConstr(gp.quicksum(x[i, j, k] for j in range(N)) <= z[k], f"activation_{i}_{k}")


    # Contrainte : empêcher les boucles (pas de trajets de i à i pour chaque camion)
    for i in range(N):
        for k in range(K):
            model.addConstr(x[i, i, k] == 0, f"no_loop_{i}_{k}")

    # Contrainte : chaque centre de collecte est visité au plus une fois par un camion
    for i in range(1, N):
        model.addConstr(gp.quicksum(x[i, j, k] for j in range(N) for k in range(K)) <= 1, f"visit_once_{i}")

    # Ajout d'une contrainte de retour au dépôt (ex : le centre 0 est le dépôt)
    for k in range(K):
        model.addConstr(gp.quicksum(x[0, j, k] for j in range(1, N)) == z[k], f"start_from_depot_{k}")
        model.addConstr(gp.quicksum(x[i, 0, k] for i in range(1, N)) == z[k], f"return_to_depot_{k}")

    # Conservation du flux (si un camion visite un centre, il doit également en repartir)
    for k in range(K):
        for i in range(1, N):
            model.addConstr(gp.quicksum(x[i, j, k] for j in range(N)) == gp.quicksum(x[j, i, k] for j in range(N)),
                            f"flow_conservation_{i}_{k}")


    # Résolution du modèle
    model.Params.OutputFlag = 0
    model.optimize()

    # Affichage des résultats
    if model.status == GRB.OPTIMAL:

        #print("\nSolution optimale trouvée :")
        
        total_quantity = 0  # Initialiser la quantité totale collectée
        quantity_per_center = {i: 0 for i in range(N)}  # Dictionnaire pour stocker la quantité récoltée par chaque centre

        
        for k in range(K):
            if z[k].X > 0.5:  # Si le camion k est utilisé

                print(f"\nCamion {k + 1} utilisé :") if debug else None
                for i in range(N):
                    for j in range(N):
                        if x[i, j, k].X > 0.5:  # Si le camion parcourt l'arc (i, j)
                            print(f"  Parcours de {i} à {j} avec distance {distances[i, j]:.2f} et quantité collectée {q[i, k].X:.2f}")if debug else None
                    quantity_per_center[i] += q[i, k].X

                # Quantité totale collectée par ce camion
                camion_quantity = sum(q[i, k].X for i in range(N))
                print(f"Quantité totale collectée par le camion {k + 1}: {camion_quantity:.2f}")if debug else None
                
                # Ajouter cette quantité à la quantité totale
                total_quantity += camion_quantity
                
        
        # Afficher la quantité totale collectée par tous les camions
        print(f"\nQuantité totale collectée par tous les camions : {total_quantity:.2f}")if debug else None

        if debug : 
            # Visualisation
            plt.figure(figsize=(10, 7))
            plt.scatter(locations[:, 0], locations[:, 1], c='red', label='Centres de collecte')
            plt.scatter(locations[0, 0], locations[0, 1], c='blue', marker='s', label='Dépôt')

            for k in range(K):
                if z[k].X > 0.5:
                    for i in range(N):
                        for j in range(N):
                            if x[i, j, k].X > 0.5:
                                plt.plot([locations[i, 0], locations[j, 0]], [locations[i, 1], locations[j, 1]],
                                        label=f'Camion {k + 1}' if i == 0 and j == 1 else "")
            
            plt.legend()
            plt.title("Trajets des camions pour la collecte de sang")
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.show()
    
        return total_quantity,quantity_per_center,model.objVal





