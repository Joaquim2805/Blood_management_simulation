from simulation.demand import simulation_demand
from simulation.dispo import simulation_disp
from politics.PFA import PFA
import numpy as np
from source import recolte_sang









def complete_sim_with_peremption(t_low, t_target):
    # Définition des ensembles et paramètres
    N = 6  # Nombre de centres de collecte (y compris le dépôt)
    K = 6  # Nombre de camions disponibles
    Q = 500  # Capacité maximale de chaque camion
    alpha = 1  # Coût fixe par camion déployé
    stock_file = []  # File d'attente pour gérer la péremption
    stock_ages = []  # Liste pour suivre l'âge des stocks
    locations = np.array([
        [0, 0],  # Dépôt
        [2, 3],
        [5, 2],
        [1, 4],
        [6, 5],
        [3, 2]
    ])

    final_cost = []
    stock_history = []
    recourse_count = []
    peremption = []

    # Simulation sur une année
    for m in range(1, 13):  # Parcours des mois
        for week in range(4):  # Parcours des semaines dans un mois
            # Simulation des disponibilités
            dispo = simulation_disp(N - 1, [6] * (N - 1), m)  # Disponibilités par centre
            dispo = np.insert(dispo, 0, 0)  # Ajouter le dépôt
            S_min = PFA(sum(stock_file), m, dispo, t_low, t_target)  # Ajustement du seuil minimal
            S_c = 160
            recourse_flag = False

            # Calcul de la récolte de sang
            r, qt, val_obj = recolte_sang(N, K, Q, S_min, alpha, locations, dispo, False)

            # Mise à jour du stock
            stock_file.append(r)  # Ajout de la collecte au stock
            stock_ages.append(0)  # Initialiser l'âge du stock à 0 (semaine courante)
            temp_cost = val_obj

            # Consommation quotidienne
            for day in range(7):
                demand_d = int(simulation_demand(1, m))  # Demande quotidienne

                # Vérifier si des stocks risquent de périmer (âge > 2 semaines)
                impending_expiry = any(age > 2 for age in stock_ages)

                if sum(stock_file) >= S_c:  # Si la file de stock n'est pas vide
                    # Si des stocks risquent de périmer, on déclenche une collecte supplémentaire
                    if impending_expiry:
                        recourse_flag = True
                        S_min2 = PFA(sum(stock_file), m, dispo, t_low, t_target)
                        r2, qt2, val_obj2 = recolte_sang(N, K, Q, S_min2, alpha, locations, dispo, False)
                        temp_cost += val_obj2
                        if r2 - demand_d >= 0:
                            stock_file.append(r2 - demand_d)
                            stock_ages.append(0)  # Réinitialiser l'âge du nouveau stock
                        break  # On sort de la boucle de consommation car la collecte a été déclenchée

                    # Consommer le stock par ordre FIFO
                    remaining_demand = demand_d
                    for i in range(len(stock_file)):
                        if stock_file[i] >= remaining_demand:
                            stock_file[i] -= remaining_demand
                            remaining_demand = 0
                            break
                        else:
                            remaining_demand -= stock_file[i]
                            stock_file[i] = 0

                    # Retirer les stocks épuisés
                    stock_file = [s for s in stock_file if s > 0]
                    available_stock = sum(stock_file)

                else:
                    # Fonction de recours en cas de stock insuffisant
                    recourse_flag = True
                    S_min2 = PFA(sum(stock_file), m, dispo, t_low, t_target)
                    r2, qt2, val_obj2 = recolte_sang(N, K, Q, S_min2, alpha, locations, dispo, False)
                    temp_cost += val_obj2
                    if r2 - demand_d >= 0:
                        stock_file.append(r2 - demand_d)
                        stock_ages.append(0)  # Réinitialiser l'âge du nouveau stock

            # Péremption : Supprimer les stocks âgés de plus de 3 semaines
            for i in range(len(stock_file)):
                stock_ages[i] += 1  # Incrémenter l'âge du stock
                if stock_ages[i] > 3:  # Si le stock a plus de 3 semaines
                    expired = stock_file.pop(i)  # Supprimer le stock périmé
                    stock_ages.pop(i)  # Supprimer l'âge correspondant
                    peremption.append(expired)
                    break  # Sortir de la boucle après avoir enlevé un stock périmé

            # Mise à jour du stock total
            S = sum(stock_file)
            if S == 0:
                print("STOCK ZERO ERREUR")
            stock_history.append(S)

            if recourse_flag:
                recourse_count.append(1)
            else:
                recourse_count.append(0)

            final_cost.append(temp_cost)

    return final_cost, stock_history, recourse_count, peremption









def complete_sim_without_peremption(t_low, t_target):
    # Définition des ensembles et paramètres
    N = 6  # Nombre de centres de collecte (y compris le dépôt)
    K = 6  # Nombre de camions disponibles
    Q = 500  # Capacité maximale de chaque camion
    alpha = 1  # Coût fixe par camion déployé
    stock_file = []  # File d'attente pour gérer la péremption
    locations = np.array([
        [0, 0],  # Dépôt
        [2, 3],
        [5, 2],
        [1, 4],
        [6, 5],
        [3, 2]
    ])

    final_cost = []
    stock_history= []
    recourse_count = []
    peremption = []

    # Simulation sur une année
    for m in range(1, 13):  # Parcours des mois
        #print(f"\nMois : {m}")
        for week in range(4):  # Parcours des semaines dans un mois
            # Simulation des disponibilités
            dispo = simulation_disp(N - 1, [5] * (N - 1), m)  # Disponibilités par centre
            dispo = np.insert(dispo, 0, 0)  # Ajouter le dépôt
            S_min = PFA(sum(stock_file),m,dispo,t_low, t_target)  # Ajustement du seuil minimal
            S_c = 160 
            recourse_flag = False
            #print(f"  Semaine {week + 1}")
            #print(f"  Disponibilités : {dispo}")

            # Calcul de la récolte de sang
            r ,qt, val_obj= recolte_sang(N, K, Q, S_min, alpha, locations, dispo, False)
            #print(f"  Sang récolté : {r}")
            #print("Sang collecté dans chaque centre : ",qt)
            #print("Valeur obj finale : ",val_obj)

            # Mise à jour du stock
            stock_file.append(r)  # Ajout de la collecte au stock
            temp_cost = val_obj
            #print(f"  Stock ajouté à la file : {r}")

            # Consommation quotidienne
            for day in range(7):
                demand_d = int(simulation_demand(1, m))  # Demande quotidienne
                #print(f"\nDemande sang jour {day + 1} : {demand_d}, Stock disponible : {sum(stock_file)}")

                if sum(stock_file) >= S_c:  # Si la file de stock n'est pas vide

                    # Consommer le stock par ordre FIFO
                    remaining_demand = demand_d
                    for i in range(len(stock_file)):
                        if stock_file[i] >= remaining_demand:
                            stock_file[i] -= remaining_demand
                            remaining_demand = 0
                            break
                        else:
                            remaining_demand -= stock_file[i]
                            stock_file[i] = 0

                    # Retirer les stocks épuisés
                    stock_file = [s for s in stock_file if s > 0]
                    available_stock = sum(stock_file)
                    #print(f"    Stock disponible après consommation : {available_stock}")

                else:
                    #print(" Seuil critique atteint. Déclenchement de la fonction de recours")
                    recourse_flag = True
                    S_min2 = PFA(sum(stock_file),m,dispo,t_low, t_target)
                    r2 ,qt2, val_obj2= recolte_sang(N, K, Q, S_min2, alpha, locations, dispo, False)
                    temp_cost += val_obj2
                    #print("Sang récolté 2 : ",r2)
                    if r2-demand_d >= 0:
                        stock_file.append(r2-demand_d)

            if recourse_flag:
                recourse_count.append(1)
            else:
                recourse_count.append(0)

            # Péremption : Supprimer les stocks âgés de plus de 3 semaines
            print("TAILLE STOCK FILE : ",len(stock_file))
            if len(stock_file) > 3:
                expired = stock_file.pop(0)
                #print(f"  Stock périmé retiré : {expired}")
                peremption.append(expired)

            # Mise à jour du stock total
            S = sum(stock_file)
            stock_history.append(S)
            #print(f"  Nouveau stock après consommation et péremption : {S}")
            if S == 0:
                temp_cost+=1000
            #print("\n***********\n")
            final_cost.append(temp_cost)

            #break
        #break
        
    #print("COUT FINAL :", np.sum(final_cost))
    return final_cost,stock_history,recourse_count,peremption

#final_cost,stock_history,recourse_count = complete_sim()