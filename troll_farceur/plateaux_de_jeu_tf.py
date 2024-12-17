import tkinter as tk
from PIL import Image, ImageTk
import random
import json
import os
from fonction_troll_farceur import round_rectangle
import moteur_tf
import pygame

# Création et configuration de la fenêtre
class plateau(tk.Toplevel):
    def __init__(self, root, app, info_joueurs):
        super().__init__(root)
        self.app = app
        self.info_joueurs = info_joueurs
        self.peut_lancer = True
        self.title("le troll farceur")
        self.geometry("800x700")

        self.canvas = tk.Canvas(self, width=800, height=700)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.bg_image = tk.PhotoImage(file = "troll_farceur/images/mine_ia.png")
        self.canvas.create_image(0,0,anchor="nw", image=self.bg_image)

        pygame.mixer.init()
        pygame.mixer.music.load("troll_farceur/son/son_tf.mp3")
        pygame.mixer.music.play(-1)

        try:
            with open('troll_farceur/actuel.json', 'r') as joueur_actuel:
                self.actuel = json.load(joueur_actuel)
            self.joueur_actuel = (self.actuel['dernier_joueur'] + 1) % len(self.info_joueurs)
            if self.joueur_actuel == 0 and self.info_joueurs[self.joueur_actuel][5] == False:
                self.lancer_de_des_troll()
            else:
                self.peut_lancer = True
        except FileNotFoundError:
            self.joueur_actuel = 1
            self.actuel = {"dernier_joueur": 1}
       
        ### mettre les ligne 23 a 29 en commentaire pour utiliser les vrais lancer de dès
        # Chargez le fichier JSON pour les scénario
        #with open('troll_farceur/tricheur_tf.json', 'r') as file:
        #    self.scenarios = json.load(file)
    
        # Choisissez le scénario approprié
        #self.scenario_actuel = self.scenarios["scenario_predefini_3J"]
        #self.index_lancer = 0

        # On stock et charge les images sinon elles ne s'affiche pas
        self.images = []
        # Chargement des images
        self.charger_images()
        # dictionnaire vide
        self.dict_position = {}
        self.pions = {}
        #On dessine le plateau de jeu (après le dictionnaire vide sinon ça marche pas)
        self.dessiner_rectangles(70, 70, 63)

        self.interface()

    #fonction pour charger les images
    def charger_images(self):
        # Chargez l'image des potions
        image_potion = Image.open("troll_farceur/images/potion_ia.jpg")
        image_potion = image_potion.resize((69, 69), Image.LANCZOS)
        self.photo_potion = ImageTk.PhotoImage(image_potion)

        # Chargez l'image du portail
        image_portail = Image.open("troll_farceur/images/portail_ia.jpg")
        image_portail = image_portail.resize((69, 69), Image.LANCZOS)
        self.photo_portail = ImageTk.PhotoImage(image_portail)

        # Chargez l'image du coffre
        image_coffre = Image.open("troll_farceur/images/coffre_ia.png")
        image_coffre = image_coffre.resize((69, 69), Image.LANCZOS)
        self.photo_coffre = ImageTk.PhotoImage(image_coffre)

        # Chargez l'image des oubliettes
        image_oubliette = Image.open("troll_farceur/images/oubliette_ia.jpg")
        image_oubliette = image_oubliette.resize((69, 69), Image.LANCZOS)
        self.photo_oubliette = ImageTk.PhotoImage(image_oubliette)

        # Chargez l'image du coffre méchant
        image_coffre_mechant = Image.open("troll_farceur/images/coffre_mechant_ia.jpg")
        image_coffre_mechant = image_coffre_mechant.resize((69, 69), Image.LANCZOS)
        self.photo_coffre_mechant = ImageTk.PhotoImage(image_coffre_mechant)

        # Chargez l'image de la tête du troll qui dort
        image_dodo = Image.open("troll_farceur/images/dodo_ia.png")
        image_dodo = image_dodo.resize((69, 69), Image.LANCZOS)
        self.photo_dodo = ImageTk.PhotoImage(image_dodo)

        # Chargez l'image du piège à flèches
        image_piege = Image.open("troll_farceur/images/piege_fleches_ia.jpg")
        image_piege = image_piege.resize((69, 69), Image.LANCZOS)
        self.photo_piege = ImageTk.PhotoImage(image_piege)

        # Chargez l'image de la cuisine
        image_cuisine = Image.open("troll_farceur/images/cuisine_ia.png")
        image_cuisine = image_cuisine.resize((104, 104), Image.LANCZOS)
        self.photo_cuisine = ImageTk.PhotoImage(image_cuisine)

        # Chargez l'image de la sortie
        image_sortie = Image.open("troll_farceur/images/sortie_ia.jpg")
        image_sortie = image_sortie.resize((104, 104), Image.LANCZOS)
        self.photo_sortie = ImageTk.PhotoImage(image_sortie)

        # Chargez l'image des crottes
        image_crotte = Image.open("troll_farceur/images/crotte_ia.jpg")
        image_crotte = image_crotte.resize((69, 69), Image.LANCZOS)
        self.photo_crotte= ImageTk.PhotoImage(image_crotte)


    # fonction qui créer une image
    def creer_image(self, photo, x1, y1, x2, y2):
        image = self.canvas.create_image((x1 + x2)/2, (y1 + y2)/2, image=photo, anchor="center")
        self.images.append(photo)  # stocker l'image
        return image

    # Fonction pour dessiner le plateau du jeu de l'oie.
    def dessiner_rectangles(self, largeur, hauteur, nombre_rectangles):
        x2 = 115
        y1 = 45
        i = 0
        while i <= nombre_rectangles:
            if i == 0:
                # Affichage de la case départ
                x1 = 15 # Position x du rectangle
                y1 = 15   # Position y du rectangle
                x2 = 120  # Position x opposée
                y2 = 120 # Position y opposée
                self.creer_image(self.photo_cuisine,x1, y1, x2, y2)
                self.dict_position[i] = [x1 , y2]
                i += 1
                y1 = y1 + 35 # pour réalignée les cases suivantes
            elif 1 <= i <= 9 or 30 <= i <= 37 or 52 <= i <= 57:
                x1 = x2 + 5
                y1 = y1
                x2 = x1 + largeur
                y2 = y1 + hauteur
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="grey")
                if i == 9 or i == 36 or i == 54:
                    self.creer_image(self.photo_potion,x1, y1, x2, y2)
                elif i == 6:
                    self.creer_image(self.photo_portail,x1, y1, x2, y2)
                elif i == 31:
                    self.creer_image(self.photo_oubliette,x1, y1, x2, y2)
                elif i == 52:
                    self.creer_image(self.photo_coffre_mechant,x1, y1, x2, y2)
                elif i == 53:
                    self.creer_image(self.photo_crotte,x1, y1, x2, y2)
                else:
                    self.canvas.create_text((x2 + x1)/2, (y2 + y1)/2, text= str(i), fill=("black"), font=("Arial", 16))
                self.dict_position[i] = [x1 , y2]
                i += 1
            elif 10 <= i <= 15 or 38 <= i <= 41 or 58 <= i <= 59:
                x1 = x1
                y1 = y2 +5
                x2 = x1 + largeur
                y2 = y1 + hauteur
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="grey")
                if i == 58:
                    self.creer_image(self.photo_dodo,x1, y1, x2, y2)
                else:
                    self.canvas.create_text((x2 + x1)/2, (y2 + y1)/2, text= str(i), fill=("black"), font=("Arial", 16))
                self.dict_position[i] = [x1 , y2]
                i += 1
            elif 16 <= i <= 24 or 42 <= i <= 48 or 60 <= i <= 62:
                x1 = x1 - largeur -5
                y1 = y1
                x2 = x1 + largeur
                y2 = y1 + hauteur
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="grey")
                if i == 18 or i == 45:
                    self.creer_image(self.photo_potion,x1, y1, x2, y2)
                elif i == 19:
                    self.creer_image(self.photo_coffre,x1, y1, x2, y2)
                elif i == 42:
                    self.creer_image(self.photo_piege,x1, y1, x2, y2)
                else:
                    self.canvas.create_text((x2 + x1)/2, (y2 + y1)/2, text= str(i), fill=("black"), font=("Arial", 16))
                self.dict_position[i] = [x1 , y2]
                i += 1
            elif 25 <= i <= 29 or 49 <= i <= 51:
                x1 = x1
                y1 = y1 - hauteur - 5
                x2 = x2
                y2 = y1 + hauteur
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="grey")
                if i == 27:
                    self.creer_image(self.photo_potion,x1, y1, x2, y2)
                elif i == 26:
                    self.creer_image(self.photo_crotte,x1, y1, x2, y2)
                else:
                    self.canvas.create_text((x2 + x1)/2, (y2 + y1)/2, text= str(i), fill=("black"), font=("Arial", 16))
                self.dict_position[i] = [x1 , y2]
                i += 1
            else:
                x1 = x1 - 110
                y1 = y1 - 35
                x2 = x1 + 105
                y2 = y1 + 105
                self.creer_image(self.photo_sortie,x1, y1, x2, y2)
                self.dict_position[i] = [x1 , y2]
                i += 1

    def interface(self):
        # bouton lancé de dés
        self.lance = round_rectangle(self.canvas, 45, 640, 195, 690, radius=20, fill="grey", outline="black")
        self.lancebis = self.canvas.create_text((45 + 195)/2, (640 + 690)/2, text="Lancer les dés", font=("Arial", 16))

        # afficher la couleur et le pseudonyme du joueur actuel
        self.joueur_oval = self.canvas.create_oval(45, 595, 75, 625, fill="", outline="black")
        self.joueur_text = self.canvas.create_text((80 + 195)/2, (595 + 625)/2, text="", font=("Arial", 16))

        # afficher le résultat du lancé de dés
        self.canvas.create_polygon(240, 630, 270, 660, 240, 690, 210, 660, fill="grey", outline="black")
        self.des1 = self.canvas.create_text(240, 660, text="0", font=("Arial", 16))
        self.canvas.create_polygon(270, 580, 300, 610, 270, 640, 240, 610, fill="grey", outline="black")
        self.des2 = self.canvas.create_text(270, 610, text="0", font=("Arial", 16))

        # bouton pour continuer
        self.suivant = round_rectangle(self.canvas, 700, 600, 790, 690, radius=20, fill="grey", outline="black")
        self.suivant_txt = self.canvas.create_text((700 + 790)/2, (600 + 690)/2, text="Suivant", font=("Arial", 16))

        # rectangle qui affiche la condition de la case
        self.condition = self.canvas.create_rectangle(310, 600, 690, 690, fill="grey")
        self.condition_text = self.canvas.create_text((310 + 690)/2, (600 + 690)/2, text="", font=("Arial", 11))

        # action lier aux boutons
        self.canvas.tag_bind(self.lance, "<Button-1>", self.lancer_de_des)
        self.canvas.tag_bind(self.lancebis, "<Button-1>", self.lancer_de_des)
        self.canvas.tag_bind(self.suivant, "<Button-1>", self.joueur_suivant)
        self.canvas.tag_bind(self.suivant_txt, "<Button-1>", self.joueur_suivant)

        self.afficher_joueur_actuel()
        self.afficher_pion()

    # fonction lancer de dés basique
    def lancer_de_des(self, event):
        if self.peut_lancer:
            a = random.randint(1, 6) # le lancer de dés
            b = random.randint(1, 6)
            self.canvas.itemconfig(self.des1, text=str(a)) # affiche le résultat
            self.canvas.itemconfig(self.des2, text=str(b))
            self.peut_lancer = False  # pour ne pas lancer les dés 2 fois
            self.canvas.itemconfig(self.condition_text, text = moteur_tf.moteur(self.joueur_actuel, a, b, self.info_joueurs))
            self.actuel['dernier_joueur'] = self.joueur_actuel
            with open('troll_farceur/actuel.json', 'w') as file:
                json.dump(self.actuel, file)
    
    def lancer_de_des_troll(self):
        if self.peut_lancer:
            a = random.randint(1, 6) # le lancer de dés
            b = random.randint(1, 6)
            self.canvas.itemconfig(self.des1, text=str(a)) # affiche le résultat
            self.canvas.itemconfig(self.des2, text=str(b))
            self.peut_lancer = False  # pour ne pas lancer les dés 2 fois
            self.canvas.itemconfig(self.condition_text, text = moteur_tf.moteur(self.joueur_actuel, a, b, self.info_joueurs))
            self.actuel['dernier_joueur'] = self.joueur_actuel
            with open('troll_farceur/actuel.json', 'w') as file:
                json.dump(self.actuel, file)

    def troll_dort(self):
        self.joueur_actuel = (self.joueur_actuel + 1) % len(self.info_joueurs)
        self.peut_lancer = True # pour que le joueur suivant puisse lancer les dés
        self.afficher_joueur_actuel()
        self.canvas.itemconfig(self.condition_text, text="Lancez les dés")

    def joueur_suivant(self, event): # fonction associer au bouton "suivant"
        if not self.peut_lancer: # le joueur ne peut pas appuyer sur "suivant" s'il n'a pas lancer les dés
            self.afficher_pion()
            if self.info_joueurs[self.joueur_actuel][2] == 63:
                self.victoire(self.joueur_actuel)
            elif all(value[5] for value in self.info_joueurs.values()):
                    self.app.ouvrir_defaite()
                    os.remove('troll_farceur/info_joueurs_tf.json')
                    os.remove('troll_farceur/actuel.json')
            elif self.info_joueurs[0][5] == False and sum(value[5] for value in self.info_joueurs.values()) == len(self.info_joueurs) - 1:
                self.app.ouvrir_defaite()
                os.remove('troll_farceur/info_joueurs_tf.json')
                os.remove('troll_farceur/actuel.json')
            else:
                self.joueur_actuel = (self.joueur_actuel + 1) % len(self.info_joueurs)
                self.peut_lancer = True # pour que le joueur suivant puisse lancer les dés
                self.afficher_joueur_actuel()
                if self.info_joueurs[self.joueur_actuel][0] == "troll" and self.info_joueurs[self.joueur_actuel][5] == False:
                    self.lancer_de_des_troll()
                else:
                    self.canvas.itemconfig(self.des1, text="0") # on initialise les dés à 0
                    self.canvas.itemconfig(self.des2, text="0")
                    if self.info_joueurs[self.joueur_actuel][4] > 0:  # Vérifier si le joueur doit passer son tour
                        self.peut_lancer = False
                        self.info_joueurs[self.joueur_actuel][4] -= 1  # on passe un tour
                        self.canvas.itemconfig(self.condition_text, text="Vous devez passer votre tour")
                        with open('troll_farceur/info_joueurs_tf.json', 'w') as fichier_json:
                            json.dump(self.info_joueurs, fichier_json, indent=4)
                    elif self.info_joueurs[self.joueur_actuel][5]:  # Vérifier si le joueur est bloqué
                        self.peut_lancer = False
                        if self.info_joueurs[self.joueur_actuel][0] == "troll":
                            self.troll_dort()
                        else:
                            self.canvas.itemconfig(self.condition_text, text="Vous devez passer votre tour")
                    else:
                        self.canvas.itemconfig(self.condition_text, text="Lancez les dés") # text par défault

    def afficher_joueur_actuel(self): # Fonction associer a la précédante (elle sert a afficher le joueur actuel)
        joueur = self.info_joueurs[self.joueur_actuel]
        self.canvas.itemconfig(self.joueur_text, text=joueur[0], fill = 'white') # Affiche le nom du joueur
        couleur_joueur = joueur[1] # la couleur est stocker en deuxième position soit d'indice 1
        self.canvas.itemconfig(self.joueur_oval, fill=couleur_joueur)

    def afficher_pion(self):
        for cle in self.info_joueurs:
            joueur = self.info_joueurs[cle]
            couleur_joueur = joueur[1]
            case_pion_actuel = joueur[2]
            x_pion, y_pion = self.dict_position[case_pion_actuel]
            if cle in self.pions:
                self.canvas.delete(self.pions[cle])
            nouveau_pion = self.canvas.create_oval(x_pion, y_pion-30, x_pion+30, y_pion, fill=couleur_joueur, outline="black")
            self.pions[cle] = nouveau_pion

    def victoire(self, joueur):
        if self.info_joueurs[joueur][0] == "troll":
            self.app.ouvrir_troll()
            os.remove('troll_farceur/actuel.json')
            os.remove('troll_farceur/info_joueurs_tf.json')
        else:
            self.app.ouvrir_victoire(self.info_joueurs[joueur][0])
            os.remove('troll_farceur/info_joueurs_tf.json')
            os.remove('troll_farceur/actuel.json')