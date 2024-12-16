import tkinter as tk
from fonction_jeu_de_l_oie import round_rectangle
from tkinter import messagebox

class acceuil(tk.Toplevel):
    def __init__(self,root, app):
        super().__init__(root)
        self.app = app
        self.title("Jeu de l'oie")
        self.geometry("500x700")

        self.canvas = tk.Canvas(self, width=500, height=700, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # on initialise le nombre de joueur à 0 
        self.nombre_joueurs = tk.IntVar(value=0)

        self.creer_evenements()

        self.canvas.create_text(250, 50, text="Jeu", font=("Impact", 22))
        self.canvas.create_text(250, 100, text="de", font=("Comic sans ms", 14))
        self.canvas.create_text(250, 150, text="L'Oie", font=("Impact", 22))
        self.canvas.create_text(250, 250, text="Nombre de joueurs", font=("Comic sans ms", 14))

        # Boutons de sélection du nombre de joueurs
        for i, x in enumerate([100, 200, 300, 400], 1):
            self.canvas.create_polygon(x, 300, x-25, 325, x, 350, x+25, 325, fill="white", outline="black", tags=f"rect{i}")
            self.canvas.create_text(x, 325, text=str(i), font=("Comic sans ms", 14), tags=f"text{i}")

        # Bouton PLAY
        round_rectangle(self.canvas, 200, 425, 300, 475, radius=20, fill="white", outline="black", tags=("clickable","rect5"))
        self.canvas.create_text(250, 450, text="PLAY", font=("Impact", 18), tags=("clickable","text5"))

    def creer_evenements(self):
        for i in range(1, 5):
            self.canvas.tag_bind(f"rect{i}", "<Enter>", lambda e, i=i: self.on_enter(i))
            self.canvas.tag_bind(f"rect{i}", "<Leave>", lambda e, i=i: self.on_leave(i))
            self.canvas.tag_bind(f"rect{i}", "<Button-1>", lambda e, i=i: self.selectionner_joueurs(i))
            self.canvas.tag_bind(f"text{i}", "<Enter>", lambda e, i=i: self.on_enter(i))
            self.canvas.tag_bind(f"text{i}", "<Leave>", lambda e, i=i: self.on_leave(i))
            self.canvas.tag_bind(f"text{i}", "<Button-1>", lambda e, i=i: self.selectionner_joueurs(i))

        self.canvas.tag_bind("clickable", "<Enter>", self.on_enter_play)
        self.canvas.tag_bind("clickable", "<Leave>", self.on_leave_play)
        self.canvas.tag_bind("clickable", "<Button-1>", self.lancer_jeu)

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
            self.app.ouvrir_pseudos(self.nombre_joueurs.get())
        else:
            messagebox.showwarning("Attention", "Veuillez selectionner un nombre de joueur.")