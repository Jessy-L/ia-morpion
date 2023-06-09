import tkinter as tk
from tkinter import messagebox
import random
import numpy as np

# création de la fenetre principale  - ne pas toucher
LARG = 300
HAUT = 300

Window = tk.Tk()
Window.geometry(str(LARG)+"x"+str(HAUT))   # taille de la fenetre
Window.title("Morpion")


# création de la frame principale stockant toutes les pages
F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages
ListePages  = {}
PageActive = 0

def creerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def afficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
Frame0 = creerUnePage(0)

canvas = tk.Canvas(Frame0,width = LARG, height = HAUT, bg ="#252422" )
canvas.place(x=0,y=0)


#  Parametres du jeu
Grille = [ 
    [0,0,0],
    [0,0,0],
    [0,0,0]
]  # attention les lignes représentent les colonnes de la grille

Grille = np.array(Grille)
Grille = Grille.transpose()  # pour avoir x,y

PlayerTurn = True # True = joueur, False = IA

def gameState():
    # Victoire de l'Humain
    if(
        Grille[0][0] == 1 and Grille[0][1] == 1 and Grille[0][2] == 1 or
        Grille[1][0] == 1 and Grille[1][1] == 1 and Grille[1][2] == 1 or
        Grille[2][0] == 1 and Grille[2][1] == 1 and Grille[2][2] == 1 or
        Grille[0][0] == 1 and Grille[1][0] == 1 and Grille[2][0] == 1 or
        Grille[0][1] == 1 and Grille[1][1] == 1 and Grille[2][1] == 1 or
        Grille[0][2] == 1 and Grille[1][2] == 1 and Grille[2][2] == 1 or
        Grille[0][0] == 1 and Grille[1][1] == 1 and Grille[2][2] == 1 or
        Grille[0][2] == 1 and Grille[1][1] == 1 and Grille[2][0] == 1
    ):
        return 1
    # Victoire de l'IA
    elif(
        Grille[0][0] == 2 and Grille[0][1] == 2 and Grille[0][2] == 2 or
        Grille[1][0] == 2 and Grille[1][1] == 2 and Grille[1][2] == 2 or
        Grille[2][0] == 2 and Grille[2][1] == 2 and Grille[2][2] == 2 or
        Grille[0][0] == 2 and Grille[1][0] == 2 and Grille[2][0] == 2 or
        Grille[0][1] == 2 and Grille[1][1] == 2 and Grille[2][1] == 2 or
        Grille[0][2] == 2 and Grille[1][2] == 2 and Grille[2][2] == 2 or
        Grille[0][0] == 2 and Grille[1][1] == 2 and Grille[2][2] == 2 or
        Grille[0][2] == 2 and Grille[1][1] == 2 and Grille[2][0] == 2
    ):
        return 2
    # Match nul
    elif(
        Grille[0][0] != 0 and Grille[0][1] != 0 and Grille[0][2] != 0 and
        Grille[1][0] != 0 and Grille[1][1] != 0 and Grille[1][2] != 0 and
        Grille[2][0] != 0 and Grille[2][1] != 0 and Grille[2][2] != 0
    ):
        return 0
    # Partie en cours
    else:
        return 3

def WinningCase(): 
    if(gameState() == 1):
        canvas.itemconfig("line", fill="red")
        messagebox.showinfo("Victoire", "Vous avez gagné !")
        Window.destroy()
    elif(gameState() == 2):
        canvas.itemconfig("line", fill="yellow")
        messagebox.showinfo("Défaite", "Vous avez perdu !")
        Window.destroy()
    elif(gameState() == 0):
        canvas.itemconfig("line", fill="white")
        messagebox.showinfo("Egalité", "Match nul !")
        Window.destroy()

def calculCoupsPossibles(): 
    ListeCoupsPossibles = []
    for x in range (3):
        for y in range (3):
            if(Grille[x][y] == 0):
                ListeCoupsPossibles.append([x,y])
                print(ListeCoupsPossibles)

    return ListeCoupsPossibles

def joueurSimuleIA(Grille):
    ListeCoupsPossibles = calculCoupsPossibles()
    Resultat = []
    if(gameState() == 1 or gameState() == 2):
        return (-1,0)
    if(gameState() == 0):
        return (0,0)
    for CoupPossible in ListeCoupsPossibles:
        Grille[CoupPossible[0]][CoupPossible[1]] = 2
        R = joueurSimuleHumain(Grille)
        Resultat.append(R[0])
        Grille[CoupPossible[0]][CoupPossible[1]] = 0
        MeilleurCoupPossible = (max(Resultat),Resultat.index(max(Resultat)))
    return MeilleurCoupPossible

def joueurSimuleHumain(Grille):
    ListeCoupsPossibles = calculCoupsPossibles()
    Resultat =[]
    if(gameState() == 1 or gameState() == 2):
        return (1,0)
    if(gameState() == 0):
        return (0,0)
    for CoupPossible in ListeCoupsPossibles:
        Grille[CoupPossible[0]][CoupPossible[1]] = 1
        R = joueurSimuleIA(Grille)
        Resultat.append(R[0])
        Grille[CoupPossible[0]][CoupPossible[1]] = 0
        MeilleurCoupPossible = (min(Resultat),Resultat.index(min(Resultat)))
    return MeilleurCoupPossible

def play(x,y):        

    if (gameState() == 3) :
        if (Grille[x][y] == 0):
            Grille[x][y] = 1
            if (gameState() == 3) :
                ListeCoupsPossibles = calculCoupsPossibles()
                print(ListeCoupsPossibles)
                print(joueurSimuleIA(Grille))
                Grille[ListeCoupsPossibles[joueurSimuleIA(Grille)[1]][0]][ListeCoupsPossibles[joueurSimuleIA(Grille)[1]][1]] = 2
    else: 
        WinningCase()

# Dessine la grille de jeu
def dessine(_ = False):
        # DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")

        for i in range(4):
            canvas.create_line(
                i*100,
                0,
                i*100,
                300,
                fill="#CCC5B9",
                width="4",
                tag = "line"
            )
            canvas.create_line(
                0,
                i*100,
                300,
                i*100,
                fill="#CCC5B9",
                width="4",
                tag = "line"
            )

        for x in range(3):
            for y in range(3):
                xc = x * 100 
                yc = y * 100 
                if ( Grille[x][y] == 1):
                    canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="#EB5E28", width="4")
                    canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="#EB5E28", width="4")
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="#3E885B", width="4")
    

#  fnt appelée par un clic souris sur la zone de dessin
def mouseClick(event):

    Window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return

    print("Input : ", x,y)
    
    play(x,y)  # gestion du joueur humain et de l'IA
    
    dessine()
    
canvas.bind('<ButtonPress-1>', mouseClick)

#  Mise en place de l'interface - ne pas toucher
afficherPage(0)
dessine()

Window.mainloop()