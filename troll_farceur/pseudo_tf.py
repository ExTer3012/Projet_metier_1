import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, colorchooser
import json

class Pseudos(tk.Toplevel):
    def __init__(self, root, app, nombre_joueurs):
        super().__init__(root)
        self.app = app
        self.nombre_joueurs = nombre_joueurs
        self.title("troll_farceur")
        self.geometry("500x700")

        self.canvas = tk.Canvas(self, width=500, height=700, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.bg_image = tk.PhotoImage(file = "troll_farceur/images/mine_ia.png")
        self.canvas.create_image(0,0,anchor="nw", image=self.bg_image)

        self.info_joueurs = {}
        self.entries = []
        self.color_buttons = []
        self.colors = []

        self.canvas.create_text(250, 50, text="Entrez les pseudonymes des joueurs", font=("Comic sans ms", 14), fill="white")

        # pour chaque joueur selectionner la couleur et entrer un pseudo
        for i in range(self.nombre_joueurs):
            y = 100 + i * 80
            self.canvas.create_text(100, y, text=f"Joueur {i+1}:", font=("Comic sans ms", 12), anchor="w", fill="white")
            
            entry = tk.Entry(self, font=("Comic sans ms", 12))
            self.canvas.create_window(250, y, window=entry, width=150)
            self.entries.append(entry)

            color_button = tk.Button(self, text="Choisir couleur", command=lambda i=i: self.choose_color(i))
            self.canvas.create_window(400, y, window=color_button)
            self.color_buttons.append(color_button)
            self.colors.append("#000000")  # Couleur par défaut : noir

        button = tk.Button(self, text="Commencer la partie", command=self.valider_pseudos)
        self.canvas.create_window(250, 120 + self.nombre_joueurs * 80, window=button)

    def choose_color(self, player_index):
        color = colorchooser.askcolor(title=f"Choisissez une couleur pour le Joueur {player_index+1}")
        if color[1]:  # Si une couleur a été choisie
            self.colors[player_index] = color[1]
            self.color_buttons[player_index].config(bg=color[1])

    def valider_pseudos(self):
        self.info_joueurs[0] = [ "troll", "black", 0, 0, 0, True, True] #le troll est bloqué dés le début
        all_filled = all(entry.get().strip() for entry in self.entries if entry.winfo_exists())
        if all_filled:
            for i, entry in enumerate(self.entries):
                if entry.winfo_exists():
                    name = entry.get().strip()
                    self.info_joueurs[i+1] = [name, self.colors[i], 0, 0, 0, False, True]
            self.app.ouvrir_plateau(self.info_joueurs)
            self.save_to_json()
        else:
            messagebox.showwarning("Attention", "Veuillez entrer un pseudonyme pour chaque joueur.")

    def save_to_json(self):
        with open('troll_farceur/info_joueurs_tf.json', 'w') as fichier_json:
            json.dump(self.info_joueurs, fichier_json, indent=4)

    def destroy(self):
        for entry in self.entries:
            if entry.winfo_exists():
                entry.destroy()
        for button in self.color_buttons:
            if button.winfo_exists():
                button.destroy()
        super().destroy()