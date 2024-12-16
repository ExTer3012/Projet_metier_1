import tkinter as tk
import json
import os
from fonction_troll_farceur import round_rectangle
from tkinter import messagebox

class acceuil(tk.Toplevel):
    def __init__(self,root, app):
        super().__init__(root)
        self.app = app
        self.title("le troll farceur")
        self.geometry("500x700")

        self.canvas = tk.Canvas(self, width=500, height=700, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        try:
            with open('troll_farceur/info_joueurs_tf.json', 'r') as info_joueurs:
                self.info_joueurs = json.load(info_joueurs)
            self.info_joueurs = {int(cle): valeur for cle, valeur in self.info_joueurs.items()}
        except FileNotFoundError:
            self.info_joueurs = False

        # on initialise le nombre de joueur à 0 
        self.nombre_joueurs = tk.IntVar(value=0)

        self.creer_evenements()

        self.bg_image = tk.PhotoImage(file = "troll_farceur/images/mine_ia.png")
        self.canvas.create_image(0,0,anchor="nw", image=self.bg_image)


        self.canvas.create_text(250, 125, text="Le Troll Farceur", font=("Impact", 30), fill='white')
        self.canvas.create_text(250, 250, text="Nombre de joueurs", font=("Comic sans ms", 14), fill='white')

        # Boutons de sélection du nombre de joueurs
        for i, x in enumerate([100, 200, 300, 400], 1):
            self.canvas.create_polygon(x, 300, x-25, 325, x, 350, x+25, 325, fill="white", outline="black", tags=f"rect{i}")
            self.canvas.create_text(x, 325, text=str(i), font=("Comic sans ms", 14), tags=f"text{i}")

        # Bouton PLAY
        round_rectangle(self.canvas, 200, 425, 300, 475, radius=20, fill="white", outline="black", tags=("clickable","rect5"))
        self.canvas.create_text(250, 450, text="PLAY", font=("Impact", 18), tags=("clickable","text5"))
        
        # Bouton partie sauvegardé
        if self.info_joueurs:
            round_rectangle(self.canvas, 190, 500, 310, 550, radius=20, fill="white", outline="black", tags=("clickable2","rect6"))
            self.canvas.create_text(250, 525, text="REPRENDRE", font=("Impact", 18), tags=("clickable2","text6"))

    def creer_evenements(self):
        for i in range(1, 6):
            self.canvas.tag_bind(f"rect{i}", "<Enter>", lambda e, i=i: self.on_enter(i))
            self.canvas.tag_bind(f"rect{i}", "<Leave>", lambda e, i=i: self.on_leave(i))
            self.canvas.tag_bind(f"rect{i}", "<Button-1>", lambda e, i=i: self.selectionner_joueurs(i))
            self.canvas.tag_bind(f"text{i}", "<Enter>", lambda e, i=i: self.on_enter(i))
            self.canvas.tag_bind(f"text{i}", "<Leave>", lambda e, i=i: self.on_leave(i))
            self.canvas.tag_bind(f"text{i}", "<Button-1>", lambda e, i=i: self.selectionner_joueurs(i))

        self.canvas.tag_bind("clickable", "<Enter>", self.on_enter_play)
        self.canvas.tag_bind("clickable", "<Leave>", self.on_leave_play)
        self.canvas.tag_bind("clickable", "<Button-1>", self.lancer_jeu)
        self.canvas.tag_bind("clickable2", "<Enter>", self.on_enter_rep)
        self.canvas.tag_bind("clickable2", "<Leave>", self.on_leave_rep)
        self.canvas.tag_bind("clickable2", "<Button-1>", self.reprendre_jeu)

    def on_enter(self, i):
        self.canvas.itemconfig(f"rect{i}", outline="yellow", width=3)
        self.canvas.itemconfig(f"text{i}", fill="yellow")

    def on_leave(self, i):
        if self.nombre_joueurs.get() != i:
            self.canvas.itemconfig(f"rect{i}", outline="black", width=1)
            self.canvas.itemconfig(f"text{i}", fill="black")

    def on_enter_play(self, event):
        self.canvas.itemconfig("rect5", outline="yellow", width=3)
        self.canvas.itemconfig("text5", fill="yellow")

    def on_leave_play(self, event):
        self.canvas.itemconfig("rect5", outline="black", width=1)
        self.canvas.itemconfig("text5", fill="black")

    def on_enter_rep(self, event):
        self.canvas.itemconfig("rect6", outline="yellow", width=3)
        self.canvas.itemconfig("text6", fill="yellow")

    def on_leave_rep(self, event):
        self.canvas.itemconfig("rect6", outline="black", width=1)
        self.canvas.itemconfig("text6", fill="black")

    def selectionner_joueurs(self, nombre):
        self.nombre_joueurs.set(nombre)
        for i in range(1, 5):
            if i == nombre:
                color = "yellow"
                width = 3
            else:
                color = "black"
                width = 1
            self.canvas.itemconfig(f"rect{i}", outline=color, width=width)
            self.canvas.itemconfig(f"text{i}", fill=color)

    def lancer_jeu(self, event):
        if self.nombre_joueurs.get() > 0:
            if self.info_joueurs:
                os.remove('troll_farceur/actuel.json')
            self.app.ouvrir_pseudos(self.nombre_joueurs.get())
        else:
            messagebox.showwarning("Attention", "Veuillez selectionner un nombre de joueur.")

    def reprendre_jeu(self, event):
        self.app.ouvrir_plateau(self.info_joueurs)