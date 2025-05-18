# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Imports ---------------------------------------------------------------------
from tkinter import Tk, Frame, LEFT, RIGHT, Button, BOTH, Canvas, TOP, \
                    BOTTOM, ALL
import random

COULEURS = ["red", "blue", "green", "yellow", "magenta", "orange", "cyan"]

def initialiser_plateau(n, nb_boules):
    """Renvoie la grille correspondant à la configuration initiale du jeu: un
    plateau ne contenant que nb_boules de couleurs aléatoires, placées
    aléatoirement."""
    plateau = [[None for _ in range(n)] for _ in range(n)]
    positions = [(i, j) for i in range(n) for j in range(n)]
    random.shuffle(positions)
    for _ in range(nb_boules):
        i, j = positions.pop()
        plateau[i][j] = random.choice(COULEURS)
    return plateau

def cases_accessibles(M, i, j, deja_visitees):
    """Renvoie l'ensemble des cases accessibles à partir de la case M[i][j].
    Une case est accessible si elle est vide et si on peut y amener la boule
    en case M[i][j] uniquement par des déplacements horizontaux ou verticaux.
    """
    if (i, j) in deja_visitees:
        return set()
    deja_visitees.add((i, j))
    accessibles = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(M) and 0 <= nj < len(M[0]) and M[ni][nj] is None:
            accessibles.add((ni, nj))
            accessibles.update(cases_accessibles(M, ni, nj, deja_visitees))

    return accessibles

def detections_horizontales(M):
    """Renvoie, pour chacune des lignes, les coordonnées des cases contenues
    dans une sous-ligne de taille au moins 5."""
    a_retirer = set()
    for i, ligne in enumerate(M):
        compteur = 1
        for j in range(1, len(ligne)):
            if ligne[j] is not None and ligne[j] == ligne[j - 1]:
                compteur += 1
            else:
                if compteur >= 5:
                    a_retirer.update({(i, k) for k in range(j - compteur, j)})
                compteur = 1
        if compteur >= 5:
            a_retirer.update({(i, k) for k in range(len(ligne) - compteur, len(ligne))})
    return a_retirer

def detections_verticales(M):
    """Renvoie, pour chacune des colonnes, les coordonnées des cases contenues
    dans une sous-colonne de taille au moins 5."""
    a_retirer = set()
    for j in range(len(M[0])):  # Parcourir les colonnes
        compteur = 1
        for i in range(1, len(M)):
            if M[i][j] is not None and M[i][j] == M[i - 1][j]:
                compteur += 1
            else:
                if compteur >= 5:
                    a_retirer.update({(k, j) for k in range(i - compteur, i)})
                compteur = 1
        if compteur >= 5:
            a_retirer.update({(k, j) for k in range(len(M) - compteur, len(M))})
    return a_retirer

def detections_diagonales(M):
    """Renvoie, pour chacune des diagonales, les coordonnées des cases contenues
    dans une sous-diagonale de taille au moins 5."""
    a_retirer = set()
    n, m = len(M), len(M[0])

    # Diagonales de haut-gauche à bas-droite
    for k in range(-n + 1, m):
        diag = []
        for i in range(max(0, -k), min(n, m - k)):
            diag.append((i, i + k))
        compteur = 1
        for idx in range(1, len(diag)):
            x1, y1 = diag[idx - 1]
            x2, y2 = diag[idx]
            if M[x1][y1] is not None and M[x1][y1] == M[x2][y2]:
                compteur += 1
            else:
                if compteur >= 5:
                    a_retirer.update(diag[idx - compteur:idx])
                compteur = 1
        if compteur >= 5:
            a_retirer.update(diag[len(diag) - compteur:])

    # Diagonales de haut-droite à bas-gauche
    for k in range(n + m - 1):
        diag = []
        for i in range(max(0, k - m + 1), min(n, k + 1)):
            diag.append((i, k - i))
        compteur = 1
        for idx in range(1, len(diag)):
            x1, y1 = diag[idx - 1]
            x2, y2 = diag[idx]
            if M[x1][y1] is not None and M[x1][y1] == M[x2][y2]:
                compteur += 1
            else:
                if compteur >= 5:
                    a_retirer.update(diag[idx - compteur:idx])
                compteur = 1
        if compteur >= 5:
            a_retirer.update(diag[len(diag) - compteur:])

    return a_retirer

# =============================================================================
# PARTIE A NE PAS MODIFIER ====================================================
# =============================================================================

def boules_suivantes(nb_boules):
    """Renvoie nb_boules boules de couleur aléatoire qui serviront de
    boules suivantes."""
    return [random.choice(COULEURS) for _ in range(nb_boules)]

class ColorLinesGUI:
    """Interface pour le jeu Color Lines."""
    def __init__(self):
        """Initialise l'interface."""
        # initialisation des structures de données ----------------------------
        self.dim_plateau = 9       # nombre de lignes et de colonnes du plateau
        self.hauteur_plateau = self.largeur_plateau = 288
        self.cote_case = self.hauteur_plateau // self.dim_plateau
        self.plateau = []
        self.destinations_ok = set()      # destinations valides pour une boule
        self.nb_boules_init = 3
        self.nb_boules_suivantes = 3
        self.case_selectionnee = None  # la case cliquée au coup précédent, qui
                                       # contient la boule qu'on veut déplacer

        # initialisation des éléments graphiques ------------------------------
        self.window = Tk()  # la fenêtre principale
        self.window.resizable(0, 0)  # empêcher les redimensionnements
        self.partie_haut = Frame(
            self.window, width=self.largeur_plateau,
            height=self.hauteur_plateau
        )
        self.partie_haut.pack(side=TOP)
        self.partie_bas = Frame(self.window)
        self.partie_bas.pack(side=BOTTOM)

        # le canevas affichant le plateau de jeu
        self.plateau_affiche = Canvas(self.partie_haut,
                                      width=self.largeur_plateau,
                                      height=self.hauteur_plateau)
        self.plateau_affiche.pack()
        self.plateau_affiche.bind('<ButtonPress-1>', self.clic_plateau)

        # AFFICHAGE des boules suivantes:
        self.boules_suivantes = boules_suivantes(self.nb_boules_suivantes)
        self.boules_suivantes_affiche = Canvas(
            self.partie_bas, width=self.largeur_plateau // 3, height=32
        )
        self.boules_suivantes_affiche.pack(side=LEFT)

        # AFFICHAGE du score:
        self.score = 0
        self.score_affiche = Canvas(
            self.partie_bas, width=self.largeur_plateau // 3, height=32
        )
        self.score_affiche.pack(side=RIGHT)

        self.reinitialiser_jeu()

        # les boutons
        self.btn = Button(self.partie_bas, text='Réinitialiser',
                          command=self.reinitialiser_jeu)
        self.btn.pack(fill=BOTH, expand=1)

        self.window.title('Color Lines')
        self.window.mainloop()

    def dessiner_boule(self, i, j, couleur):
        """Dessine la boule de couleur donnée par self.plateau[j][i]."""
        bord = 3
        self.plateau_affiche.create_oval(
            i * self.cote_case + bord, j * self.cote_case + bord,
            (i + 1) * self.cote_case - bord,
            (j + 1) * self.cote_case - bord,
            outline="black", fill=couleur
        )

    def rafraichir_plateau(self):
        """Redessine le plateau de jeu à afficher."""
        self.plateau_affiche.delete(ALL)
        # tracer les cases
        for i in range(self.dim_plateau):
            for j in range(self.dim_plateau):
                couleur_case = "light gray"  # couleur par défaut d'une case
                if (j, i) in self.destinations_ok:
                    couleur_case = "light green"
                self.plateau_affiche.create_rectangle(
                    i * self.cote_case, j * self.cote_case,
                    (i + 1) * self.cote_case,
                    (j + 1) * self.cote_case,
                    outline="black", fill=couleur_case
                )
                if self.plateau[j][i] is not None:          # afficher la boule
                    self.dessiner_boule(i, j, self.plateau[j][i])

        self.plateau_affiche.create_line(0, 0, 0, self.largeur_plateau,
                                         width=3)
        self.plateau_affiche.create_line(0, 0, self.hauteur_plateau, 0,
                                         width=3)

    def rafraichir_boules_suivantes(self):
        """Montre les couleurs des boules suivantes."""
        self.boules_suivantes_affiche.delete(ALL)
        self.boules_suivantes_affiche.create_text(
            self.cote_case // 2 + 18, 6,
            text="Suivantes:"
        )
        bord = 8
        for i, boule in enumerate(self.boules_suivantes):
            self.boules_suivantes_affiche.create_oval(
                i * self.cote_case + bord,  self.cote_case // 4 + bord,
                (i + 1) * self.cote_case - bord,
                self.cote_case * 5 // 4 - bord,
                outline="black", fill=boule
            )

    def rafraichir_score(self):
        """Rafraîchit l'AFFICHAGE des scores."""
        self.score_affiche.delete(ALL)
        self.score_affiche.create_text(self.cote_case // 2 + 4, 6,
                                       text="Score:")
        self.score_affiche.create_text(
            self.largeur_plateau // 3 - self.cote_case // 2,
            self.cote_case // 2 + 10,
            text=str(self.score)
        )

    def clic_plateau(self, event):
        """Récupère les coordonnées de la case sélectionnée, et joue le coup
        correspondant s'il est permis."""
        (j, i) = (event.x // self.cote_case, event.y // self.cote_case)
        if self.plateau[i][j]:
            if self.destinations_ok:
                self.destinations_ok = set()
            else:
                cases_visitees = set()
                self.destinations_ok = cases_accessibles(self.plateau, i, j,
                                                         cases_visitees)
                self.destinations_ok.discard((i, j))
                self.case_selectionnee = (i, j)
            self.rafraichir_plateau()
        else:
            if self.case_selectionnee:
                if (i, j) in self.destinations_ok:
                    self.deplacer_boule(
                        self.case_selectionnee[0], self.case_selectionnee[1],
                        i, j
                    )
                    if not self.retirer_series():
                        cases_libres = [
                            (x, y) for x in range(self.dim_plateau)
                            for y in range(self.dim_plateau)
                            if not self.plateau[x][y]
                        ]
                        random.shuffle(cases_libres)
                        for boule in self.boules_suivantes:
                            if not cases_libres:
                                break
                            x_b, y_b = cases_libres.pop()
                            self.plateau[x_b][y_b] = boule
                        self.boules_suivantes = boules_suivantes(self.nb_boules_suivantes)
                        self.rafraichir_jeu()
                        self.retirer_series()
                else:
                    self.destinations_ok = set()
                self.rafraichir_jeu()
                self.case_selectionnee = None

    def deplacer_boule(self, i, j, p, q):
        """Déplace la boule en coordonnées (i, j) vers les coordonnées (p, q)
        si possible."""
        if (p, q) in self.destinations_ok:
            self.plateau[p][q] = self.plateau[i][j]
            self.plateau[i][j] = None
            self.destinations_ok = set()

    def rafraichir_jeu(self):
        """Rafraîchit le plateau de jeu, les boules suivantes et le score."""
        self.rafraichir_plateau()
        self.rafraichir_boules_suivantes()
        self.rafraichir_score()

    def reinitialiser_jeu(self):
        """Réinitialise le plateau de jeu et les scores."""
        self.destinations_ok = set()
        self.score = 0
        self.boules_suivantes = boules_suivantes(self.nb_boules_suivantes)
        self.reinitialiser_plateau()
        self.rafraichir_boules_suivantes()
        self.rafraichir_score()

    def reinitialiser_plateau(self):
        """Réinitialise le plateau de jeu."""
        self.plateau = initialiser_plateau(
            self.dim_plateau, self.nb_boules_init
        )
        self.plateau_affiche.delete(ALL)
        if self.plateau is not None:
            self.rafraichir_plateau()

    def retirer_series(self):
        """Retire du plateau les alignements verticaux, horizontaux et
        diagonaux d'au moins cinq boules de la même couleur, et met à jour le
        score du joueur. Renvoie True si l'on a retiré quelque chose, False
        sinon."""
        cases_a_retirer = detections_horizontales(self.plateau)
        cases_a_retirer.update(detections_verticales(self.plateau))
        cases_a_retirer.update(detections_diagonales(self.plateau))
        if cases_a_retirer:
            self.score += 2 * len(cases_a_retirer)
            for (i, j) in cases_a_retirer:
                self.plateau[i][j] = None
            return True
        return False

if __name__ == "__main__":
    ColorLinesGUI()
