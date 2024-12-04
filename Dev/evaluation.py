from simulation.demand import simulation_demand
from simulation.dispo import simulation_disp
from politics.PFA import PFA
import numpy as np
from source import recolte_sang
from politics.DL import direct_lookahead








def complete_sim_with_peremption(t_low, t_target,locations,N,K,Q,alpha,policy,a,b):

    stock_file = []  # File d'attente pour gérer la péremption
    stock_ages = []  # Liste pour suivre l'âge des stocks

    final_cost = []
    stock_history = []
    recourse_count = []
    peremption = []
    d_hist = []
    d_bar = 0
    d_hist2 = []
    d_bar2 = 0


    Q_h = 1300

    # Simulation sur une année
    for m in range(1, 13):  # Parcours des mois
        for week in range(4):  # Parcours des semaines dans un mois
            # Simulation des disponibilités
            dispo = simulation_disp(N - 1, [6] * (N - 1), m)  # Disponibilités par centre
            dispo = np.insert(dispo, 0, 0)  # Ajouter le dépôt
            if policy=="PFA":
                S_min = PFA(sum(stock_file), m, dispo, t_low, t_target)  # Ajustement du seuil minimal
            elif policy =="DL":
                S_min = direct_lookahead(d_bar,a,b,m)

            S_c = 160
            recourse_flag = False

            if sum(stock_file)+S_min > Q_h:
                S_min = Q_h - (sum(stock_file)+S_min)

            # Calcul de la récolte de sang
            r, qt, val_obj = recolte_sang(N, K, Q, S_min, alpha, locations, dispo, False)

            # Mise à jour du stock
            stock_file.append(r)  # Ajout de la collecte au stock
            stock_ages.append(0)  # Initialiser l'âge du stock à 0 (semaine courante)
            temp_cost = val_obj
            temp_mean = 0

            # Consommation quotidienne
            for day in range(7):
                demand_d = int(simulation_demand(1, m))  # Demande quotidienne
                temp_mean+=demand_d

                # Vérifier si des stocks risquent de périmer (âge > 2 semaines)
                impending_expiry = any(age > 2 for age in stock_ages)



                if sum(stock_file) >= S_c:  # Si la file de stock n'est pas vide
                    # Si des stocks risquent de périmer, on déclenche une collecte supplémentaire
                    if impending_expiry:
                        recourse_flag = True
                        if policy == "PFA":
                            S_min2 = PFA(sum(stock_file), m, dispo, t_low, t_target)
                        else :
                            if m in [4,5,6,7,8,9]:
                                al = -0.4
                            else :
                                al=0
                            S_min2 = demand_d*(7-day) + demand_d*(7-day)*al
                        
                        if sum(stock_file)+S_min2 > Q_h:
                            S_min2 = Q_h - (sum(stock_file)+S_min2)


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
                    if policy == "PFA":
                        S_min2 = PFA(sum(stock_file), m, dispo, t_low, t_target)
                    else :
                            if m in [4,5,6,7,8,9]:
                                al = -0.8
                            else :
                                al=0
                            S_min2 = demand_d*(7-day) + demand_d*(7-day)*al
                        

                    


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
            
            d_hist.append(temp_mean)
            d_bar = np.mean(d_hist)
            # Mise à jour du stock total
            S = sum(stock_file)
            
            if S == 0:
                temp_cost+=10
                #print("STOCK ZERO ERREUR")
        
            stock_history.append(S)

            if recourse_flag:
                recourse_count.append(1)
            else:
                recourse_count.append(0)

            final_cost.append(temp_cost)

    return final_cost, stock_history, recourse_count, peremption









def complete_sim_without_peremption(t_low, t_target,locations,N,K,Q,alpha):
    
    stock_file = []  # File d'attente pour gérer la péremption
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
            r ,qt, val_obj= recolte_sang(N, K, Q, S_min, alpha, locations, dispo, True)
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
