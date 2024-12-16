    # fonction lancer de dés basique
    def lancer_de_des(self, event):
        if self.peut_lancer:
            a = random.randint(1, 6) # le lancer de dés
            b = random.randint(1, 6)
            self.canvas.itemconfig(self.des1, text=str(a)) # affiche le résultat
            self.canvas.itemconfig(self.des2, text=str(b))
            self.peut_lancer = False  # pour ne pas lancer les dés 2 fois
            self.canvas.itemconfig(self.condition_text, text = moteur.moteur(self.joueur_actuel, a, b, self.info_joueurs))

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