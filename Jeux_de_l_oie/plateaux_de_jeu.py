import tkinter as tk
from PIL import Image, ImageTk
import random
import json
from fonction_jeu_de_l_oie import round_rectangle
import moteur

# Création et configuration de la fenêtre
class plateau(tk.Toplevel):
    def __init__(self, root, app, info_joueurs):
        super().__init__(root)
        self.app = app
        self.info_joueurs = info_joueurs
        self.joueur_actuel = 0
        self.peut_lancer = True
        self.title("Jeu de l'oie")
        self.geometry("800x700")

        self.canvas = tk.Canvas(self, width=800, height=700, bg="lightblue")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        ### mettre les ligne 23 a 29 en commentaire pour utiliser les vrais lancer de dès
        # Chargez le fichier JSON pour les scénario
        with open('Jeux_de_l_oie/tricheur.json', 'r') as file:
            self.scenarios = json.load(file)
    
        # Choisissez le scénario approprié
        self.scenario_actuel = self.scenarios["scenario_predefini_3J"]
        self.index_lancer = 0

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
        # Chargez l'image de l'oie
        image_oie = Image.open("Jeux_de_l_oie/images/oie.jfif")
        image_oie = image_oie.resize((69, 69), Image.LANCZOS)
        self.photo_oie = ImageTk.PhotoImage(image_oie)

        # Chargez l'image du pont
        image_pont = Image.open("Jeux_de_l_oie/images/pont.jfif")
        image_pont = image_pont.resize((69, 69), Image.LANCZOS)
        self.photo_pont = ImageTk.PhotoImage(image_pont)

        # Chargez l'image du nid (hotel)
        image_nid = Image.open("Jeux_de_l_oie/images/nid.jfif")
        image_nid = image_nid.resize((69, 69), Image.LANCZOS)
        self.photo_nid = ImageTk.PhotoImage(image_nid)

        # Chargez l'image du puits
        image_puit = Image.open("Jeux_de_l_oie/images/puit.jfif")
        image_puit = image_puit.resize((69, 69), Image.LANCZOS)
        self.photo_puit = ImageTk.PhotoImage(image_puit)

        # Chargez l'image de la prison
        image_prison = Image.open("Jeux_de_l_oie/images/prison.jfif")
        image_prison = image_prison.resize((69, 69), Image.LANCZOS)
        self.photo_prison = ImageTk.PhotoImage(image_prison)

        # Chargez l'image de la tête de mort
        image_mort = Image.open("Jeux_de_l_oie/images/mort.jfif")
        image_mort = image_mort.resize((69, 69), Image.LANCZOS)
        self.photo_mort = ImageTk.PhotoImage(image_mort)

        # Chargez l'image du labirynte
        image_laby = Image.open("Jeux_de_l_oie/images/laby.jfif")
        image_laby = image_laby.resize((69, 69), Image.LANCZOS)
        self.photo_laby = ImageTk.PhotoImage(image_laby)

        # Chargez l'image des dès
        image_des = Image.open("Jeux_de_l_oie/images/dès.jfif")
        image_des = image_des.resize((69, 69), Image.LANCZOS)
        self.photo_des = ImageTk.PhotoImage(image_des)

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
                x1 = 10 # Position x du rectangle
                y1 = 10   # Position y du rectangle
                x2 = 115  # Position x opposée
                y2 = 115 # Position y opposée
                round_rectangle(self.canvas, x1, y1, x2, y2, radius=20, outline="red", fill="black")
                self.canvas.create_text((x2 + x1)/2, (y2 + y1)/2, text="Départ", fill=("white"), font=("Arial", 16))
                self.dict_position[i] = [x1 , y2]
                i += 1
                y1 = y1 + 35 # pour réalignée les cases suivantes
            elif 1 <= i <= 9 or 30 <= i <= 37 or 52 <= i <= 57:
                x1 = x2 + 5
                y1 = y1
                x2 = x1 + largeur
                y2 = y1 + hauteur
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")
                if i == 9 or i == 36 or i == 54:
                    self.creer_image(self.photo_oie,x1, y1, x2, y2)
                elif i == 6:
                    self.creer_image(self.photo_pont,x1, y1, x2, y2)
                elif i == 31:
                    self.creer_image(self.photo_puit,x1, y1, x2, y2)
                elif i == 52:
                    self.creer_image(self.photo_prison,x1, y1, x2, y2)
                elif i == 53:
                    self.creer_image(self.photo_des,x1, y1, x2, y2)
                else:
                    self.canvas.create_text((x2 + x1)/2, (y2 + y1)/2, text= str(i), fill=("black"), font=("Arial", 16))
                self.dict_position[i] = [x1 , y2]
                i += 1
            elif 10 <= i <= 15 or 38 <= i <= 41 or 58 <= i <= 59:
                x1 = x1
                y1 = y2 +5
                x2 = x1 + largeur
                y2 = y1 + hauteur
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")
                if i == 12:
                    self.creer_image(self.photo_pont,x1, y1, x2, y2)
                elif i == 58:
                    self.creer_image(self.photo_mort,x1, y1, x2, y2)
                else:
                    self.canvas.create_text((x2 + x1)/2, (y2 + y1)/2, text= str(i), fill=("black"), font=("Arial", 16))
                self.dict_position[i] = [x1 , y2]
                i += 1
            elif 16 <= i <= 24 or 42 <= i <= 48 or 60 <= i <= 62:
                x1 = x1 - largeur -5
                y1 = y1
                x2 = x1 + largeur
                y2 = y1 + hauteur
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")
                if i == 18 or i == 45:
                    self.creer_image(self.photo_oie,x1, y1, x2, y2)
                elif i == 19:
                    self.creer_image(self.photo_nid,x1, y1, x2, y2)
                elif i == 42:
                    self.creer_image(self.photo_laby,x1, y1, x2, y2)
                else:
                    self.canvas.create_text((x2 + x1)/2, (y2 + y1)/2, text= str(i), fill=("black"), font=("Arial", 16))
                self.dict_position[i] = [x1 , y2]
                i += 1
            elif 25 <= i <= 29 or 49 <= i <= 51:
                x1 = x1
                y1 = y1 - hauteur - 5
                x2 = x2
                y2 = y1 + hauteur
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")
                if i == 27:
                    self.creer_image(self.photo_oie,x1, y1, x2, y2)
                elif i == 26:
                    self.creer_image(self.photo_des,x1, y1, x2, y2)
                else:
                    self.canvas.create_text((x2 + x1)/2, (y2 + y1)/2, text= str(i), fill=("black"), font=("Arial", 16))
                self.dict_position[i] = [x1 , y2]
                i += 1
            else:
                x1 = x1 - 110
                y1 = y1 - 35
                x2 = x1 + 105
                y2 = y1 + 105
                round_rectangle(self.canvas, x1, y1, x2, y2, radius=20, outline="red", fill="black")
                self.canvas.create_text((x2 + x1)/2, (y2 + y1)/2, text="Arrivée", fill=("white"), font=("Arial", 16))
                self.dict_position[i] = [x1 , y2]
                i += 1

    def interface(self):
        # bouton lancé de dés
        self.lance = round_rectangle(self.canvas, 45, 640, 195, 690, radius=20, fill="white", outline="black")
        self.lancebis = self.canvas.create_text((45 + 195)/2, (640 + 690)/2, text="Lancer les dés", font=("Arial", 16))

        # afficher la couleur et le pseudonyme du joueur actuel
        self.joueur_oval = self.canvas.create_oval(45, 595, 75, 625, fill="", outline="black")
        self.joueur_text = self.canvas.create_text((80 + 195)/2, (595 + 625)/2, text="", font=("Arial", 16))

        # afficher le résultat du lancé de dés
        self.canvas.create_polygon(240, 630, 270, 660, 240, 690, 210, 660, fill="white", outline="black")
        self.des1 = self.canvas.create_text(240, 660, text="0", font=("Arial", 16))
        self.canvas.create_polygon(270, 580, 300, 610, 270, 640, 240, 610, fill="white", outline="black")
        self.des2 = self.canvas.create_text(270, 610, text="0", font=("Arial", 16))

        # bouton pour continuer
        self.suivant = round_rectangle(self.canvas, 700, 600, 790, 690, radius=20, fill="white", outline="black")
        self.suivant_txt = self.canvas.create_text((700 + 790)/2, (600 + 690)/2, text="Suivant", font=("Arial", 16))

        # rectangle qui affiche la condition de la case
        self.condition = self.canvas.create_rectangle(310, 600, 690, 690, fill="white")
        self.condition_text = self.canvas.create_text((310 + 690)/2, (600 + 690)/2, text="", font=("Arial", 11))

        # action lier aux boutons
        self.canvas.tag_bind(self.lance, "<Button-1>", self.lancer_de_des)
        self.canvas.tag_bind(self.lancebis, "<Button-1>", self.lancer_de_des)
        self.canvas.tag_bind(self.suivant, "<Button-1>", self.joueur_suivant)
        self.canvas.tag_bind(self.suivant_txt, "<Button-1>", self.joueur_suivant)

        self.afficher_joueur_actuel()
        self.afficher_pion()

    # fonction lancer de dés tricheur
    def lancer_de_des(self, event):
        if self.peut_lancer and self.index_lancer < len(self.scenario_actuel):
            lancer = self.scenario_actuel[self.index_lancer]
            a = lancer["des1"]
            b = lancer["des2"]
            self.canvas.itemconfig(self.des1, text=str(a))
            self.canvas.itemconfig(self.des2, text=str(b))
            self.peut_lancer = False
            self.canvas.itemconfig(self.condition_text, text = moteur.moteur(self.joueur_actuel, a, b, self.info_joueurs))
            self.index_lancer += 1

    def joueur_suivant(self, event): # fonction associer au bouton "suivant"
        if not self.peut_lancer: # le joueur ne peut pas appuyer sur "suivant" s'il n'a pas lancer les dés
            self.afficher_pion()
            if self.info_joueurs[self.joueur_actuel][2] == 63:
                self.app.ouvrir_victoire(self.info_joueurs[self.joueur_actuel][0])
            else:
                if all(value[5] for value in self.info_joueurs.values()):
                        self.app.ouvrir_defaite()
                else:
                    self.joueur_actuel = (self.joueur_actuel + 1) % len(self.info_joueurs)
                    self.peut_lancer = True # pour que le joueur suivant puisse lancer les dés
                    self.afficher_joueur_actuel()
                    self.canvas.itemconfig(self.des1, text="0") # on initialise les dés à 0
                    self.canvas.itemconfig(self.des2, text="0")
                    if self.info_joueurs[self.joueur_actuel][4]:  # Vérifier si le joueur doit passer son tour
                        self.peut_lancer = False
                        self.info_joueurs[self.joueur_actuel][4] = False  # Réinitialiser le statut "passer tour"
                        self.canvas.itemconfig(self.condition_text, text="Vous devez passer votre tour")
                        with open('Jeux_de_l_oie/info_joueurs.json', 'w') as fichier_json:
                            json.dump(self.info_joueurs, fichier_json, indent=4)
                    elif self.info_joueurs[self.joueur_actuel][5]:  # Vérifier si le joueur est bloqué
                        self.peut_lancer = False
                        self.canvas.itemconfig(self.condition_text, text="Vous devez passer votre tour")
                    else:
                        self.canvas.itemconfig(self.condition_text, text="Lancez les dés") # text par défault

    def afficher_joueur_actuel(self): # Fonction associer a la précédante (elle sert a afficher le joueur actuel)
        joueur = self.info_joueurs[self.joueur_actuel]
        self.canvas.itemconfig(self.joueur_text, text=joueur[0])  # Affiche le nom du joueur
        couleur_joueur = joueur[1] # la couleur est stocker en deuxième position soit d'indice 1
        self.canvas.itemconfig(self.joueur_oval, fill=couleur_joueur)

    def afficher_pion(self):
        joueur = self.info_joueurs[self.joueur_actuel]
        couleur_joueur = joueur[1]
        case_pion_actuel = joueur[2]
        x_pion, y_pion = self.dict_position[case_pion_actuel]
        # Supprimez l'ancien pion du joueur actuel s'il existe
        if self.joueur_actuel in self.pions:
            self.canvas.delete(self.pions[self.joueur_actuel])
        # Créez un nouveau pion à la nouvelle position
        nouveau_pion = self.canvas.create_oval(x_pion, y_pion-30, x_pion+30, y_pion, fill=couleur_joueur, outline="black")
        # Stockez le nouveau pion dans le dictionnaire
        self.pions[self.joueur_actuel] = nouveau_pion
