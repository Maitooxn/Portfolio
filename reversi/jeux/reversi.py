#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Imports ---------------------------------------------------------------------
from tkinter import Tk, Frame, LEFT, RIGHT, Button, BOTH, Canvas, TOP, \
                    BOTTOM, ALL
import tkinter.font

# Variables globales ----------------------------------------------------------
TAILLE_PLATEAU = 512

def initialiser_grille(n):
    """Renvoie la grille correspondant à la configuration initiale du jeu."""
    grille = [[None for _ in range(n)] for _ in range(n)]
    milieu = n // 2
    grille[milieu - 1][milieu - 1] = False  # Joueur 1 (noir)
    grille[milieu][milieu] = False  # Joueur 1 (noir)
    grille[milieu - 1][milieu] = True  # Joueur 2 (rouge)
    grille[milieu][milieu - 1] = True  # Joueur 2 (rouge)
    return grille

def score(M, joueur):
    """Renvoie le score du joueur, c'est-à-dire le nombre de cases de M qu'il
    possède."""
    return sum(row.count(joueur) for row in M)

def case_jouable(M, i, j):
    """Renvoie True si la case est jouable, False sinon."""
    if M[i][j] is not None:
        return False
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            ni, nj = i + di, j + dj
            if 0 <= ni < len(M) and 0 <= nj < len(M) and M[ni][nj] is not None:
                return True
    return False

def detecter_extremites(M, i, j):
    """Renvoie les "extrémités", c'est-à-dire les cases qui donnent lieu à un
    encadrement avec M[i][j]."""
    extremites = set()
    joueur = M[i][j]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for di, dj in directions:
        ni, nj = i + di, j + dj
        while 0 <= ni < len(M) and 0 <= nj < len(M):
            if M[ni][nj] == joueur:
                extremites.add((ni, nj))
                break
            elif M[ni][nj] is None:
                break
            ni += di
            nj += dj
    return extremites

def retournements(M, i, j):
    """Examine quels éléments forment un encadrement avec M[i][j], et renverse
    les pions qui doivent l'être."""
    joueur = M[i][j]
    extremites = detecter_extremites(M, i, j)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for (ei, ej) in extremites:
        di = (ei - i) // max(abs(ei - i), 1)
        dj = (ej - j) // max(abs(ej - j), 1)
        ni, nj = i + di, j + dj
        while (ni, nj) != (ei, ej):
            M[ni][nj] = joueur
            ni += di
            nj += dj


# =============================================================================
# PARTIE A NE PAS MODIFIER ====================================================
# =============================================================================

class ReversiGUI(object):
    """Interface pour le jeu de Reversi."""
    def __init__(self):
        """Initialise l'interface."""
        # initialisation des structures de données ----------------------------
        self.dim_plateau = 8       # nombre de lignes et de colonnes du plateau
        self.hauteur_plateau = self.largeur_plateau = TAILLE_PLATEAU
        self.cote_case = self.hauteur_plateau // self.dim_plateau
        self.plateau = []

        # les deux joueurs sont désignés respectivement par False et True
        self.joueur = True  # d'après les règles, c'est "noir" qui commence
        self.couleurs = ["red", "black"]

        # initialisation des éléments graphiques ------------------------------
        self.window = Tk()  # la fenêtre principale
        self.window.resizable(False, False)  # empêcher les redimensionnements
        self.partie_haut = Frame(
            self.window, width=self.largeur_plateau,
            height=self.hauteur_plateau
        )
        self.partie_haut.pack(side=TOP)
        self.partie_bas = Frame(self.window)
        self.partie_bas.pack(side=BOTTOM)

        # le canevas affichant le plateau de jeu
        self.plateau_affiche = Canvas(
            self.partie_haut, width=self.largeur_plateau,
            height=self.hauteur_plateau
        )
        self.plateau_affiche.pack()
        self.plateau_affiche.bind('<ButtonPress-1>', self.clic_plateau)

        # affichage des scores:
        self.scores = [
            Canvas(
                self.partie_bas,
                width=self.largeur_plateau // self.dim_plateau,
                height=self.hauteur_plateau // self.dim_plateau
            ),
            Canvas(
                self.partie_bas,
                width=self.largeur_plateau // self.dim_plateau,
                height=self.hauteur_plateau // self.dim_plateau
            )
        ]
        self.scores[0].pack(side=LEFT)
        self.scores[1].pack(side=RIGHT)

        self.reinitialiser_jeu()

        # les boutons
        self.btn = Button(
            self.partie_bas, text='Réinitialiser',
            command=self.reinitialiser_jeu
        )
        self.btn.pack(fill=BOTH, expand=1)

        self.window.title('Reversi - tour du joueur  1')

        self.window.mainloop()

    def rafraichir_plateau(self):
        """Redessine le plateau de jeu à afficher."""
        # tracer les pions
        bord = 3
        for i in range(self.dim_plateau):
            for j in range(self.dim_plateau):
                case = self.plateau[j][i]
                if case is not None:  # afficher le pion
                    self.plateau_affiche.create_oval(
                        i * self.cote_case + bord, j * self.cote_case + bord,
                        (i + 1) * self.cote_case - bord,
                        (j + 1) * self.cote_case - bord,
                        outline=self.couleurs[case], fill=self.couleurs[case]
                    )

    def rafraichir_scores(self):
        """Rafraîchit l'affichage des scores."""
        bord = 3
        for i in range(len(self.scores)):
            self.scores[i].delete(ALL)
            self.scores[i].create_oval(
                bord, bord, self.cote_case - bord, self.cote_case - bord,
                outline=self.couleurs[i], fill=self.couleurs[i]
            )
            self.scores[i].create_text(
                self.cote_case // 2, self.cote_case // 2,
                text=str(score(self.plateau, i)),
                font=tkinter.font.Font(family="Courier", size=12,
                                       weight=tkinter.font.BOLD),
                fill="white"
            )

    def clic_plateau(self, event):
        """Récupère les coordonnées de la case sélectionnée, et joue le coup
        correspondant s'il est permis."""
        (j, i) = (event.x // self.cote_case, event.y // self.cote_case)

        if case_jouable(self.plateau, i, j):
            self.plateau[i][j] = self.joueur     # insérer le pion
            self.joueur = not self.joueur        # changer de joueur
            retournements(self.plateau, i, j)    # appliquer les retournements
            self.rafraichir_plateau()             # afficher les changements
            self.rafraichir_scores()              # afficher les nouveaux scores
            self.window.title(
                'Reversi - tour du joueur  ' + ('1' if self.joueur else '2')
            )

    def reinitialiser_jeu(self):
        """Réinitialise le plateau de jeu et les scores."""
        self.joueur = True  # d'après les règles, c'est "noir" qui commence
        self.reinitialiser_plateau()
        self.rafraichir_scores()

    def reinitialiser_plateau(self):
        """Réinitialise le plateau de jeu."""
        # réinitialiser la matrice
        self.plateau = initialiser_grille(self.dim_plateau)
        # réinitialiser l'affichage
        self.plateau_affiche.delete(ALL)
        self.tracer_grille()
        if self.plateau is not None:
            self.rafraichir_plateau()

    def tracer_grille(self):
        """Affiche la grille du plateau sur le canevas."""
        for i in range(self.dim_plateau + 1):
            self.plateau_affiche.create_line(
                i * self.cote_case, 0, i * self.cote_case, self.hauteur_plateau
            )
            self.plateau_affiche.create_line(
                0, i * self.cote_case, self.largeur_plateau, i * self.cote_case
            )


# Programme principal --------------------------------------------------------
if __name__ == "__main__":
    ReversiGUI()
