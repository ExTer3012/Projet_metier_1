import json

def moteur(joueur, des1, des2, info_joueurs):
    with open('Jeux_de_l_oie/regles.json', 'r', encoding='utf-8') as fichier_regles:
        regles = json.load(fichier_regles)
    joueur_info = info_joueurs[joueur]
    ancienne_position = joueur_info[2]
    lancer = des1 + des2
    new_position = ancienne_position + lancer
    message = ""
    check = True

    if new_position == 63:
        message = "Félicitations ! Vous avez gagné !"
    else:
        while check == True:
            if new_position > 63:
                new_position = 63 - (new_position - 63)
                message += f"Vous avez dépassé la case 63, \nretour à la case {new_position}\n"
            #stock dans des nouvelles variables pour simplification
            regle = regles[str(new_position)]
            type_regle = regle['type_regles']
            joueur_present = case_occuper(new_position, info_joueurs, joueur)
            if joueur_info[6] == True and lancer == 9: # premier lancer
                if des1 == 3 or des1 == 6:
                    new_position = 26
                    joueur_info[6] = False
                    message = f"\nVous avez de la chance,\nvous avancez directement à la case {new_position}."
                else:
                    new_position = 53
                    joueur_info[6] = False
                    message = f"\nVous avez de la chance,\nvous avancez directement à la case {new_position}."
            elif type_regle == 1: # déplacement vers une case fixe
                message += regle['message']
                new_position = regle['case_de_destination']
            elif type_regle == 2: #oie
                message += regle['message']
                new_position += lancer
            elif type_regle == 3: # hotel
                check = False
                joueur_info[4] = True
                message += regle['message']
            elif type_regle == 4: # puit/prison
                check = False
                if joueur_present != None:
                    info_joueurs[joueur_present][5] = False
                    if new_position == 31: #si puit
                        joueur_info[5] = True
                        message += regle['message'] + regle['message_suite']
                    else: #sinon prison
                        message += regle['message'] + regle['message_suite']
                else:
                    joueur_info[5] = True
                    message += regle['message']
            elif joueur_present != None and new_position != 0: #on peut être à plusieurs sur certaine case
                if info_joueurs[joueur_present][2] == info_joueurs[joueur_present][3]: # cas rare de boucle infini à cause du dépassement de 63
                    new_position = info_joueurs[joueur_present][3] - 1
                else:
                    new_position = info_joueurs[joueur_present][3]
                message = f"Case occupée. \nVous êtes renvoyé à la position {new_position}."
            else:
                if message == "":
                    message += regle['message'] + f"\nVous avancez à la case {new_position}."
                check = False
        # réinitialisation du test du premier lancer si retour case départ
        if new_position == 0:
            joueur_info[6] = True
        else:
            joueur_info[6] = False
    # mise à jour du dictionaire
    joueur_info[3] = ancienne_position
    joueur_info[2] = new_position
    info_joueurs[joueur] = joueur_info
    with open('Jeux_de_l_oie/info_joueurs.json', 'w') as fichier_json:
        json.dump(info_joueurs, fichier_json, indent=4)
    return message

def case_occuper(position, info_joueurs, joueur):
    for key, value in info_joueurs.items():
        if position == value[2] and key != joueur:
            return key
    return None
