import tkinter as tk
from fonction_jeu_de_l_oie import round_rectangle

class Defaite(tk.Toplevel):
    def __init__(self,root, app):
        super().__init__(root)
        self.app = app
        self.title("Jeu de l'oie")
        self.geometry("500x700")

        self.canvas = tk.Canvas(self, width=500, height=700, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.create_text(200, 50, text="Vous avez perdu !", font=("Comic sans ms", 18))
        self.creer_boutons()
        self.bind_events()

    def creer_boutons(self):
        round_rectangle(self.canvas, 300, 275, 400, 325, radius=20, fill="white", outline="black", tags=("clickable1","rect1"))
        self.canvas.create_text(350, 300, text="Quitter", font=("Impact", 12), tags=("clickable1","text1"))
        round_rectangle(self.canvas, 5, 275, 150, 325, radius=20, fill="white", outline="black", tags=("clickable2","rect2"))
        self.canvas.create_text(75, 300, text="Nouvelle Partie", font=("Impact", 12), tags=("clickable2","text2"))

    def bind_events(self):
        for item in ["rect1", "text1"]:
            self.canvas.tag_bind(item, "<Enter>", self.on_enter1)
            self.canvas.tag_bind(item, "<Leave>", self.on_leave1)
        for item in ["rect2", "text2"]:
            self.canvas.tag_bind(item, "<Enter>", self.on_enter2)
            self.canvas.tag_bind(item, "<Leave>", self.on_leave2)
        self.canvas.tag_bind("clickable1", "<Button-1>", self.quitter)
        self.canvas.tag_bind("clickable2", "<Button-1>", self.nouvelle_partie)

    def on_enter1(self, event):
        self.canvas.itemconfig("rect1", outline="yellow", width=3)
        self.canvas.itemconfig("text1", fill="yellow")

    def on_leave1(self, event):
        self.canvas.itemconfig("rect1", outline="black", width=1)
        self.canvas.itemconfig("text1", fill="black")

    def on_enter2(self, event):
        self.canvas.itemconfig("rect2", outline="yellow", width=3)
        self.canvas.itemconfig("text2", fill="yellow")

    def on_leave2(self, event):
        self.canvas.itemconfig("rect2", outline="black", width=1)
        self.canvas.itemconfig("text2", fill="black")

    def quitter(self, event):
        self.app.fermer()

    def nouvelle_partie(self, event):
        self.app.ouvrir_acceuil()
