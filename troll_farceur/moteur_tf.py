import json
import pygame
import time

def moteur(joueur, des1, des2, info_joueurs):
    with open('troll_farceur/regles_tf.json', 'r', encoding='utf-8') as fichier_regles:
        regles = json.load(fichier_regles)
    joueur_info = info_joueurs[joueur]
    ancienne_position = joueur_info[2]
    lancer = des1 + des2
    new_position = ancienne_position + lancer
    message = ""
    message_troll = ""
    check = True

    if joueur_info[0] == "troll":
        message_troll = "le troll se déplace. "

    if new_position == 63:
        message = "Félicitations ! Vous avez gagné !"
    else:
        while check == True:
            if new_position > 63:
                new_position = 63 - (new_position - 63)
                message = f"Vous avez dépassé la case 63. Retour à la case {new_position}"
            #stock dans des nouvelles variables pour simplification
            regle = regles[str(new_position)]
            type_regle = regle['type_regles']
            joueur_present = case_occuper(new_position, info_joueurs, joueur)
            if joueur_info[6] == True and lancer == 9: # premier lancer
                if des1 == 3 or des1 == 6:
                    new_position = 26
                    joueur_info[6] = False
                    message = f"\nVous avez de la chance,\nvous avancez directement à la case {new_position}.\n"
                else:
                    new_position = 53
                    joueur_info[6] = False
                    message = f"\nVous avez de la chance,\nvous avancez directement à la case {new_position}.\n"
            elif type_regle == 1: # déplacement vers une case fixe
                if new_position == 58:
                    if joueur_info[0] != "troll":
                        if info_joueurs[0][5] == True:
                            message += "\nVous êtes horrifié en découvrant que le Troll est\nsomnambule. Soudain il vous attrape et cours vers les\ncuisines avec vous sous le bras."
                            new_position = regle['case_de_destination']
                            info_joueurs[0][5] = False
                            pygame.mixer.init()
                            pygame.mixer.music.load("troll_farceur/son/Fuyez.mp3")
                            pygame.mixer.music.play(loops=0)
                            time.sleep(3)
                            pygame.mixer.init()
                            pygame.mixer.music.load("troll_farceur/son/son_apres_troll.mp3")
                            pygame.mixer.music.play(-1)
                        else:
                            message += regle['message']
                            new_position = regle['case_de_destination']
                    else:
                        check = False
                elif joueur_info[0] != "troll":
                    message += regle['message']
                    new_position = regle['case_de_destination']
                else:
                    if new_position == 6:
                        new_position = regle['case_de_destination']
                    else:
                        check = False
            elif type_regle == 2: #potion
                message += regle['message']
                new_position += lancer
            elif type_regle == 3 and joueur_info[0] != "troll": # coffre
                check = False
                joueur_info[4] = 2
                message += regle['message']
            elif type_regle == 4 and joueur_info[0] != "troll": # oubliette/mimique
                check = False
                if joueur_present != None:
                    info_joueurs[joueur_present][5] = False
                    if new_position == 31: #si oubliette
                        joueur_info[5] = True
                        message += regle['message'] + regle['message_suite']
                    else: #sinon mimique
                        message += regle['message_suite']
                else:
                    joueur_info[5] = True
                    message += regle['message']
            elif joueur_present != None and new_position != 0: #on peut être à plusieurs sur certaine case
                if joueur_info[0] == "troll":
                    info_joueurs[joueur_present][2] = 0
                    message_troll = f"Le troll vous a attrapé. \nVous êtes renvoyé en cuisine."
                    check = False
                else:
                    if info_joueurs[joueur_present][2] == info_joueurs[joueur_present][3]: # cas rare de boucle infini à cause du dépassement de 63
                        new_position = info_joueurs[joueur_present][3] - 1
                    else:
                        new_position = info_joueurs[joueur_present][3]
                    message += f"Case occupée. \nVous êtes renvoyé à la position {new_position}."
            else: #type regle = 0 et aucun joueur présent
                if message == "":
                    message = regle['message'] + f"\nVous avancez à la case {new_position}."
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
    with open('troll_farceur/info_joueurs_tf.json', 'w') as fichier_json:
        json.dump(info_joueurs, fichier_json, indent=4)
    if message_troll != "":
        return message_troll
    else:
        return message

def case_occuper(position, info_joueurs, joueur):
    for key, value in info_joueurs.items():
        if position == value[2] and key != joueur:
            return key
    return None