import tkinter as tk
from acceuil import acceuil
from pseudo import Pseudos
from plateaux_de_jeu import plateau
from victoire import Victoire
from defaite import Defaite

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Cache la fenêtre principale
        self.fenetre_actuelle = None
        self.ouvrir_acceuil()

    def ouvrir_acceuil(self):
        if self.fenetre_actuelle:
            self.fenetre_actuelle.destroy()
        self.fenetre_actuelle = acceuil(self.root, self)

    def ouvrir_pseudos(self, nombre_joueurs):
        if self.fenetre_actuelle:
            self.fenetre_actuelle.destroy()
        self.fenetre_actuelle = Pseudos(self.root, self, nombre_joueurs)
        
    def ouvrir_plateau(self, info_joueurs):
        if self.fenetre_actuelle:
            self.fenetre_actuelle.destroy()
        self.fenetre_actuelle = plateau(self.root, self, info_joueurs)

    def ouvrir_victoire(self, joueur_gagnant):
        if self.fenetre_actuelle:
            self.fenetre_actuelle.destroy()
        self.fenetre_actuelle = Victoire(self.root, self, joueur_gagnant)

    def ouvrir_defaite(self):
        if self.fenetre_actuelle:
            self.fenetre_actuelle.destroy()
        self.fenetre_actuelle = Defaite(self.root, self)

    def fermer(self):
        if self.fenetre_actuelle:
            self.fenetre_actuelle.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()