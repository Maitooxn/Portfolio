from fltk import *
import random
import time
import json
import os
from itertools import product

# Dimensions de la fenêtre
LARGEUR_FENETRE = 400
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.
HAUTEUR_FENETRE   = 800 
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.
NB_COLONNES = 12
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
NB_LIGNES = 24
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
COULEURS_BLOCS = ["orange", "lightblue", "lightcoral", "lavender", "lightgreen", "beige"]
# Une liste contenant les couleurs des blocs du jeu. Chaque bloc sera affiché avec l'une d'elles.

# Polyominos standards
POLYOMINOS_STANDARDS = {
# Voici les pièces standards du jeu Tetris (appelées polyominos).
# Chaque pièce est une liste de listes représentant des blocs (1 pour un bloc, 0 pour un vide).
    'ligne': [[1], [1], [1], [1]],
    'forme_L': [[0, 1, 0], [0, 1, 0], [0, 1, 1]],
    'inversé_L': [[0, 1, 0], [0, 1, 0], [1, 1, 0]],
    'forme_Z': [[1, 1, 0], [0, 1, 1]],
    'carre': [[1, 1], [1, 1]],
    'forme_Z_inversé': [[0, 1, 1], [1, 1, 0]],
    'croix': [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
}


def lire_polyominos_corrige(fichier):
    """Lit les polyominos à partir d'un fichier et les structure correctement."""
    try:
        with open(fichier, "r") as f:
            lignes = f.readlines()
    except FileNotFoundError:
        raise ValueError("Fichier de polyominos introuvable.")
    
    polyominos = []
    polyomino_courant = []
    
    for ligne in lignes:
        ligne = ligne.strip()
        if ligne == "":
            if polyomino_courant:  # Ajouter le polyomino courant s'il existe
                polyominos.append(polyomino_courant)
                polyomino_courant = []
        else:
            polyomino_courant.append([1 if c == '+' else 0 for c in ligne])
    
    if polyomino_courant:  # Ajouter le dernier polyomino s'il n'a pas été ajouté
        polyominos.append(polyomino_courant)
    
    if not polyominos:  # Vérifier si des polyominos ont été chargés
        raise ValueError("Aucun polyomino valide trouvé dans le fichier.")
    
    return polyominos


def menu_principal():
    """Affiche le menu principal et retourne le mode sélectionné."""
    cree_fenetre(400, 300)  # Taille de la fenêtre principale
    efface_tout()
    rectangle(0, 0, 400, 300, remplissage="white")
    texte(200, 50, "Choisissez un mode de jeu", taille=20, ancrage="center", couleur="black")

    # Bouton Standard
    rectangle(50, 100, 180, 150, remplissage="lightblue")
    texte(115, 125, "Standard", taille=16, ancrage="center", couleur="black")

    # Bouton Polyominos
    rectangle(220, 100, 350, 150, remplissage="lightgreen")
    texte(285, 125, "Polyominos", taille=16, ancrage="center", couleur="black")

    # Bouton Pourrissement
    rectangle(50, 180, 180, 230, remplissage="lightpink")
    texte(115, 205, "Pourrissement", taille=16, ancrage="center", couleur="black")

    # Bouton IA
    rectangle(220, 180, 350, 230, remplissage="orange")
    texte(285, 205, "IA", taille=16, ancrage="center", couleur="black")

    while True:
        ev = attend_ev()
        if type_ev(ev) == "ClicGauche":
            x, y = abscisse(ev), ordonnee(ev)

            # Mode Standard
            if 50 <= x <= 180 and 100 <= y <= 150:
                ferme_fenetre()
                return "standard"

            # Mode Polyominos
            elif 220 <= x <= 350 and 100 <= y <= 150:
                ferme_fenetre()
                initialiser_fenetre()

                # Choix entre fichier ou génération dynamique
                efface_tout()
                texte(200, 50, "Comment charger les polyominos ?", taille=16, ancrage="center", couleur="black")

                # Bouton "Depuis un fichier"
                rectangle(50, 100, 200, 150, remplissage="lightblue")
                texte(125, 125, "Depuis un fichier", taille=12, ancrage="center", couleur="black")

                # Bouton "Générer dynamiquement"
                rectangle(220, 100, 370, 150, remplissage="lightgreen")
                texte(295, 125, "Générer dynamiquement", taille=12, ancrage="center", couleur="black")

                choix_mode = None
                mise_a_jour()

                # Boucle pour attendre le choix
                while choix_mode is None:
                    ev = attend_ev()
                    if type_ev(ev) == "ClicGauche":
                        x, y = abscisse(ev), ordonnee(ev)
                        if 50 <= x <= 200 and 100 <= y <= 150:
                            choix_mode = "fichier"
                        elif 220 <= x <= 370 and 100 <= y <= 150:
                            choix_mode = "dynamique"

                # Charger les polyominos
                if choix_mode == "fichier":
                    polyominos = lire_polyominos_corrige("polyominos.txt")
                elif choix_mode == "dynamique":
                    # Générer dynamiquement
                    n = 5  # Taille par défaut (modifiable selon les besoins)
                    polyominos = generer_polyominos(n)

                # Vérification pour débogage
                print("Polyominos utilisés :", polyominos)

                # Démarrer le jeu avec les polyominos chargés ou générés
                demarrer_jeu(polyominos)
                return

            # Mode Pourrissement
            elif 50 <= x <= 180 and 180 <= y <= 230:
                ferme_fenetre()
                return "pourrissement"

            # Mode IA
            elif 220 <= x <= 350 and 180 <= y <= 230:
                ferme_fenetre()
                return "ia"



def initialiser_fenetre():
    """Initialise la fenêtre de jeu."""
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.

def lire_polyominos(fichier):
    """Lit les polyominos à partir d'un fichier."""
    with open(fichier, "r") as f:
        lignes = f.readlines()
    polyominos = []
    polyomino_courant = []
    for ligne in lignes:
        ligne = ligne.strip()
        if ligne == "":
            if polyomino_courant:
                polyominos.append(polyomino_courant)
                polyomino_courant = []
        else:
            polyomino_courant.append([1 if c == '+' else 0 for c in ligne])
    if polyomino_courant:
        polyominos.append(polyomino_courant)
    return polyominos

def verifier_position(piece, pos_x, pos_y, grille):
    """Vérifie si la pièce peut être placée à la position donnée."""
    for i, ligne in enumerate(piece):
        for j, cellule in enumerate(ligne):
            if cellule == 1:
                x, y = pos_x + j, pos_y + i
                if x < 0 or x >= NB_COLONNES or y < 0 or y >= NB_LIGNES:
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
                    return False
                if grille[y][x][0] == 1:
                    return False
    return True

def supprimer_lignes(grille):
    """Supprime les lignes complètes de la grille et renvoie le nombre de lignes supprimées."""
    nouvelles_lignes = [ligne for ligne in grille if any(etat == 0 for etat, _ in ligne)]
    lignes_supprimees = NB_LIGNES - len(nouvelles_lignes)
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
    nouvelles_lignes = [[(0, None)] * NB_COLONNES for _ in range(lignes_supprimees)] + nouvelles_lignes
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
    return nouvelles_lignes, lignes_supprimees

def calculer_points(lignes_supprimees, niveau):
    """Calcule les points en fonction des lignes supprimées et du niveau."""
    points_par_lignes = {1: 40, 2: 100, 3: 300, 4: 500}
    multiplicateur_niveau = 1 if niveau == 1 else niveau
    return points_par_lignes.get(lignes_supprimees, 0) * multiplicateur_niveau

def gerer_evenement_clavier(ev, piece, pos_x, pos_y, grille):
    """Gère les actions clavier et retourne la nouvelle position/piece."""
    if type_ev(ev) == "Touche":
        touche_clavier = touche(ev)
        if touche_clavier == "Left" and verifier_position(piece, pos_x - 1, pos_y, grille):
            pos_x -= 1
        elif touche_clavier == "Right" and verifier_position(piece, pos_x + 1, pos_y, grille):
            pos_x += 1
        elif touche_clavier == "Down" and verifier_position(piece, pos_x, pos_y + 1, grille):
            pos_y += 1
        elif touche_clavier == "Up":
            nouvelle_piece = rotation(piece)
            if verifier_position(nouvelle_piece, pos_x, pos_y, grille):
                piece = nouvelle_piece
    return piece, pos_x, pos_y

def dessiner_grille(grille):
    """Dessine l'état actuel de la grille."""
    for y, ligne in enumerate(grille):
        for x, (etat, couleur) in enumerate(ligne):
            if etat == 1:
                rectangle(
                    x * (LARGEUR_FENETRE / NB_COLONNES),
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.
                    y * (HAUTEUR_FENETRE / NB_LIGNES),
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.
                    (x + 1) * (LARGEUR_FENETRE / NB_COLONNES),
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.
                    (y + 1) * (HAUTEUR_FENETRE / NB_LIGNES),
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.
                    remplissage=couleur
                )

def dessiner_bloc(piece, couleur, pos_x, pos_y):
    """Dessine une pièce active sur la grille."""
    for i, ligne in enumerate(piece):
        for j, cellule in enumerate(ligne):
            if cellule == 1:
                rectangle(
                    (pos_x + j) * (LARGEUR_FENETRE / NB_COLONNES),
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.
                    (pos_y + i) * (HAUTEUR_FENETRE / NB_LIGNES),
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.
                    (pos_x + j + 1) * (LARGEUR_FENETRE / NB_COLONNES),
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.
                    (pos_y + i + 1) * (HAUTEUR_FENETRE / NB_LIGNES),
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.
                    remplissage=couleur
                )

def rotation(piece):
    """Effectue une rotation horaire de 90° sur la pièce."""
    return [list(row) for row in zip(*piece[::-1])]

def supprimer_bloc_aleatoire(grille):
    """Supprime un bloc aléatoire dans la grille (pour le mode pourrissement)."""
    blocs_disponibles = [(x, y) for y in range(NB_LIGNES) for x in range(NB_COLONNES) if grille[y][x][0] == 1]
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
    if blocs_disponibles:
        x, y = random.choice(blocs_disponibles)
        grille[y][x] = (0, None)

def afficher_game_over(score, niveau, sauvegarde_possible):
    """Affiche l'écran de Game Over avec le score et le niveau."""
    efface_tout()
    rectangle(0, 0, LARGEUR_FENETRE, HAUTEUR_FENETRE, remplissage="gray")
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.
    texte(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2 - 40, "GAME OVER", taille=30, couleur="black", ancrage="center")
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.
    texte(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2, f"Score: {score}", taille=20, couleur="black", ancrage="center")
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.
    texte(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2 + 40, f"Niveau: {niveau}", taille=20, couleur="black", ancrage="center")
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.

    # Bouton "Accueil"
    rectangle(150, 500, 250, 550, remplissage="lightblue")
    texte(200, 525, "Accueil", taille=16, couleur="black", ancrage="center")
    mise_a_jour()

    while True:
        ev = attend_ev()
        if type_ev(ev) == "ClicGauche":
            x, y = abscisse(ev), ordonnee(ev)
            if 150 <= x <= 250 and 500 <= y <= 550:
                ferme_fenetre()
                main()  # Retourne au menu principal




def sauvegarde(score_actuel, niveau, vitesse, grille_jeu):

    with open("sauvegarde", 'w') as sauvegarde:
        sauvegarde.write(str(score_actuel) + "\n") 
        sauvegarde.write(str(niveau) + "\n")
        sauvegarde.write(str(vitesse) + "\n")
        sauvegarde.write("\n")

        for i in range(len(grille_jeu)):
            for j in range(len(grille_jeu[i])):
                sauvegarde.write(str(grille_jeu[i][j]))
                sauvegarde.write(" ")
            sauvegarde.write("\n")

def lecture_fichier_sauvegarde():
    with open("sauvegarde", 'r') as sauvegarde:
        # Lire les trois premières lignes pour le score, le niveau et la vitesse
        score_actuel = int(sauvegarde.readline().strip())
        niveau = int(sauvegarde.readline().strip())
        vitesse = float(sauvegarde.readline().strip())
        
        # Passer la ligne vide
        sauvegarde.readline()

        grille_jeu = []  # Initialisation de la grille
        lignes = sauvegarde.readlines()  # Lire toutes les lignes

        # Parcourir chaque ligne du fichier
        for ligne in lignes:
            ligne = ligne.strip()  # Enlever les espaces et les retours à la ligne
            if ligne:  # Ignorer les lignes vides
                liste = []  # Contiendra les éléments de la ligne
                elements = ligne.split(") ")  # Diviser les tuples sur les séparations `) `
    
                # Traiter chaque élément pour reconstruire les tuples
                for element in elements:
                    if element.endswith(")"):
                        element = element[:-1]  # Enlever la parenthèse fermante restante
                    if element.startswith("("):
                        element = element[1:]  # Enlever la parenthèse ouvrante
    
                    # Diviser en parties du tuple
                    parties = element.split(", ")
                    if len(parties) == 2:  # Vérifier qu'il y a bien deux parties
                        partie_1 = int(parties[0])  # Convertir la première partie en entier
                        partie_2 = None if parties[1] == "None" else parties[1].strip("'")
                        liste.append((partie_1, partie_2))  # Ajouter le tuple
    
                if liste:  # Ajouter la ligne à la grille si elle n'est pas vide
                    grille_jeu.append(liste)
    return score_actuel, niveau, vitesse, grille_jeu


def choix():
    efface_tout()
    rectangle(250,500,350,550, remplissage="red")  
    rectangle(50,500,150,550, remplissage="grey")  
    texte(70,50, "Reprendre partie?")
    texte(260,510, "OUI")
    texte(60,510, "NON")
    mise_a_jour()
    
    souris = attend_clic_gauche()
    
    if 250 <= souris[0] <= 350 and 500 <= souris[1] <= 550:
        demarrer_jeu(list(POLYOMINOS_STANDARDS.values()), True)
# Voici les pièces standards du jeu Tetris (appelées polyominos).
# Chaque pièce est une liste de listes représentant des blocs (1 pour un bloc, 0 pour un vide).
    
    if 50 <= souris[0] <= 150 and 500 <= souris[1] <= 550:
        demarrer_jeu(list(POLYOMINOS_STANDARDS.values()), False)
# Voici les pièces standards du jeu Tetris (appelées polyominos).
# Chaque pièce est une liste de listes représentant des blocs (1 pour un bloc, 0 pour un vide).
    
    else:
        choix()
        



def demarrer_jeu(polyominos, mode="standard", intervalle_pourrissement=5, sauvegarde_possible=False):
    """Démarre le jeu."""
    # Initialisation de la grille et des variables
    grille_jeu = [[(0, None)] * NB_COLONNES for _ in range(NB_LIGNES)]
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
    piece_active, couleur_active = random.choice(polyominos), random.choice(COULEURS_BLOCS)
# Une liste contenant les couleurs des blocs du jeu. Chaque bloc sera affiché avec l'une d'elles.
    pos_x, pos_y = NB_COLONNES // 2 - len(piece_active[0]) // 2, 0
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
    dernier_temps_deplacement = time.time()
    dernier_temps_pourrissement = time.time()
    score_actuel = 0
    niveau = 1
    vitesse = 0.5

    while True:
        temps_courant = time.time()
        if temps_courant - dernier_temps_deplacement >= vitesse:
            dernier_temps_deplacement = temps_courant
            if verifier_position(piece_active, pos_x, pos_y + 1, grille_jeu):
                pos_y += 1
            else:
                if pos_y <= 0:
                    afficher_game_over(score_actuel, niveau, sauvegarde_possible)
                    return
                for i, ligne in enumerate(piece_active):
                    for j, cellule in enumerate(ligne):
                        if cellule == 1:
                            grille_jeu[pos_y + i][pos_x + j] = (1, couleur_active)
                grille_jeu, lignes_supprimees = supprimer_lignes(grille_jeu)
                score_actuel += calculer_points(lignes_supprimees, niveau)

                # Progression de niveau basée sur le score
                if score_actuel >= niveau * 500:  # Vérifie si le score atteint le seuil
                    niveau += 1
                    vitesse = max(0.1, 0.5 / niveau)  # Ajuste la vitesse en fonction du niveau

                piece_active, couleur_active = random.choice(polyominos), random.choice(COULEURS_BLOCS)
# Une liste contenant les couleurs des blocs du jeu. Chaque bloc sera affiché avec l'une d'elles.
                pos_x, pos_y = NB_COLONNES // 2 - len(piece_active[0]) // 2, 0
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.

        if mode == "pourrissement" and temps_courant - dernier_temps_pourrissement >= intervalle_pourrissement:
            dernier_temps_pourrissement = temps_courant
            supprimer_bloc_aleatoire(grille_jeu)

        ev = donne_ev()
        if ev:
            piece_active, pos_x, pos_y = gerer_evenement_clavier(ev, piece_active, pos_x, pos_y, grille_jeu)

        if touche_pressee('space'):
            efface_tout()

            # Affichage des boutons de pause
            rectangle(150, 200, 250, 250, remplissage="lightblue")  # Reprendre
            rectangle(150, 300, 250, 350, remplissage="lightgreen")  # Accueil
            rectangle(150, 400, 250, 450, remplissage="lightpink")  # Quitter

            if sauvegarde_possible:  # Ajouter le bouton Sauvegarder seulement si possible
                rectangle(150, 500, 250, 550, remplissage="lightyellow")
                texte(200, 525, "Sauvegarder", taille=16, couleur="black", ancrage="center")

            texte(200, 225, "Reprendre", taille=16, couleur="black", ancrage="center")
            texte(200, 325, "Accueil", taille=16, couleur="black", ancrage="center")
            texte(200, 425, "Quitter", taille=16, couleur="black", ancrage="center")
            mise_a_jour()

            pause = True
            while pause:
                ev_pause = attend_ev()
                if type_ev(ev_pause) == "ClicGauche":
                    x, y = abscisse(ev_pause), ordonnee(ev_pause)
                    if 150 <= x <= 250 and 200 <= y <= 250:  # Reprendre
                        pause = False
                    elif 150 <= x <= 250 and 300 <= y <= 350:  # Accueil
                        ferme_fenetre()
                        main()  # Retourne au menu principal
                        return
                    elif 150 <= x <= 250 and 400 <= y <= 450:  # Quitter
                        ferme_fenetre()
                        exit()
                    elif sauvegarde_possible and 150 <= x <= 250 and 500 <= y <= 550:  # Sauvegarder
                        sauvegarde(score_actuel, niveau, vitesse, grille_jeu)
                        texte(200, 575, "Sauvegarde effectuée !", taille=12, couleur="black", ancrage="center")
                        mise_a_jour()
                        time.sleep(1)

        # Affichage principal
        efface_tout()
        dessiner_grille(grille_jeu)
        dessiner_bloc(piece_active, couleur_active, pos_x, pos_y)
        texte(10, 10, f"Score: {score_actuel}", taille=18, couleur="black")
        texte(10, 40, f"Niveau: {niveau}", taille=18, couleur="black")
        mise_a_jour()


def demarrer_jeu_sauvegarde(polyominos, score_actuel, niveau, vitesse, grille_jeu):
    """Démarre le jeu à partir d'une sauvegarde."""
    # Initialisation de la fenêtre
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
# Ces variables définissent les dimensions de la fenêtre de jeu (largeur et hauteur).
# On peut les ajuster si on veut modifier l'apparence de la fenêtre.

    piece_active, couleur_active = random.choice(polyominos), random.choice(COULEURS_BLOCS)
# Une liste contenant les couleurs des blocs du jeu. Chaque bloc sera affiché avec l'une d'elles.
    pos_x, pos_y = NB_COLONNES // 2 - len(piece_active[0]) // 2, 0
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
    dernier_temps_deplacement = time.time()

    while True:
        temps_courant = time.time()
        if temps_courant - dernier_temps_deplacement >= vitesse:
            dernier_temps_deplacement = temps_courant
            if verifier_position(piece_active, pos_x, pos_y + 1, grille_jeu):
                pos_y += 1
            else:
                if pos_y <= 0:
                    afficher_game_over(score_actuel, niveau, sauvegarde_possible=True)
                    return
                for i, ligne in enumerate(piece_active):
                    for j, cellule in enumerate(ligne):
                        if cellule == 1:
                            grille_jeu[pos_y + i][pos_x + j] = (1, couleur_active)
                grille_jeu, lignes_supprimees = supprimer_lignes(grille_jeu)
                score_actuel += calculer_points(lignes_supprimees, niveau)
                if score_actuel // 500 > niveau - 1:
                    niveau += 1
                    vitesse = max(0.1, vitesse - 0.05)
                piece_active, couleur_active = random.choice(polyominos), random.choice(COULEURS_BLOCS)
# Une liste contenant les couleurs des blocs du jeu. Chaque bloc sera affiché avec l'une d'elles.
                pos_x, pos_y = NB_COLONNES // 2 - len(piece_active[0]) // 2, 0
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.

        ev = donne_ev()
        if ev:
            piece_active, pos_x, pos_y = gerer_evenement_clavier(ev, piece_active, pos_x, pos_y, grille_jeu)

        if touche_pressee('space'):
            efface_tout()

            # Affichage des boutons de pause
            rectangle(150, 200, 250, 250, remplissage="lightblue")  # Reprendre
            rectangle(150, 300, 250, 350, remplissage="lightgreen")  # Accueil
            rectangle(150, 400, 250, 450, remplissage="lightpink")  # Quitter
            rectangle(150, 500, 250, 550, remplissage="yellow")  # Sauvegarder
            texte(200, 225, "Reprendre", taille=16, couleur="black", ancrage="center")
            texte(200, 325, "Accueil", taille=16, couleur="black", ancrage="center")
            texte(200, 425, "Quitter", taille=16, couleur="black", ancrage="center")
            texte(200, 525, "Sauvegarder", taille=16, couleur="black", ancrage="center")
            mise_a_jour()

            pause = True
            while pause:
                ev_pause = attend_ev()
                if type_ev(ev_pause) == "ClicGauche":
                    x, y = abscisse(ev_pause), ordonnee(ev_pause)
                    if 150 <= x <= 250 and 200 <= y <= 250:  # Reprendre
                        pause = False
                    elif 150 <= x <= 250 and 300 <= y <= 350:  # Accueil
                        ferme_fenetre()
                        main()
                        return
                    elif 150 <= x <= 250 and 400 <= y <= 450:  # Quitter
                        ferme_fenetre()
                        exit()
                    elif 150 <= x <= 250 and 500 <= y <= 550:  # Sauvegarder
                        sauvegarde(score_actuel, niveau, vitesse, grille_jeu)
                        texte(200, 575, "Sauvegarde effectuée !", taille=12, couleur="black", ancrage="center")
                        mise_a_jour()
                        time.sleep(1)

        efface_tout()
        dessiner_grille(grille_jeu)
        dessiner_bloc(piece_active, couleur_active, pos_x, pos_y)
        texte(10, 10, f"Score: {score_actuel}", taille=18, couleur="black")
        texte(10, 40, f"Niveau: {niveau}", taille=18, couleur="black")
        mise_a_jour()




def generer_polyominos(n):
    """
    Génère dynamiquement tous les polyominos de taille ≤ n.
    :param n: Taille maximale des polyominos à générer.
    :return: Liste de polyominos.
    """
    if n > 5:  # Limite pour éviter des calculs trop lourds
        raise ValueError("n trop grand ! Limite fixée à 5 pour des raisons de performance.")
    
    polyominos = []

    def formes_connexes(grille, x, y, taille_restante):
        """
        Récursion pour générer les formes connexes.
        """
        if taille_restante == 0:
            polyominos.append([ligne[:] for ligne in grille])
            return

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and grille[ny][nx] == 0:
                grille[ny][nx] = 1
                formes_connexes(grille, nx, ny, taille_restante - 1)
                grille[ny][nx] = 0

    # Générer toutes les formes à partir d'un point de départ
    for x, y in product(range(n), repeat=2):
        grille = [[0] * n for _ in range(n)]
        grille[y][x] = 1
        formes_connexes(grille, x, y, n - 1)

    # Supprimer les doublons (rotations et symétries)
    def normaliser(polyomino):
        """Renvoie une version normalisée (rotation la plus 'basse')."""
        variations = [
            tuple(map(tuple, polyomino)),
            tuple(map(tuple, list(zip(*polyomino[::-1])))),
            tuple(map(tuple, list(zip(*polyomino))[::-1])),
            tuple(map(tuple, [row[::-1] for row in polyomino])),
        ]
        return min(variations)

    polyominos_normalises = {normaliser(p) for p in polyominos}
    return [list(map(list, p)) for p in polyominos_normalises]




# Modification du main
def main():
    # Vérifie si le fichier de sauvegarde existe
    sauvegarde_disponible = os.path.exists("sauvegarde")

    # Affiche le menu principal
    mode = menu_principal()

    # Démarre le jeu selon le mode sélectionné
    if mode == "standard":
        if sauvegarde_disponible:
            # Affiche l'option pour reprendre ou démarrer une nouvelle partie
            cree_fenetre(400, 300)
            efface_tout()
            rectangle(0, 0, 400, 300, remplissage="white")
            texte(200, 50, "Voulez-vous reprendre votre sauvegarde ?", taille=16, ancrage="center", couleur="black")

            # Bouton Reprendre
            rectangle(50, 180, 180, 230, remplissage="lightblue")
            texte(115, 205, "Reprendre", taille=16, ancrage="center", couleur="black")

            # Bouton Nouvelle Partie
            rectangle(220, 180, 350, 230, remplissage="lightgreen")
            texte(285, 205, "Nouvelle Partie", taille=16, ancrage="center", couleur="black")

            while True:
                ev = attend_ev()
                if type_ev(ev) == "ClicGauche":
                    x, y = abscisse(ev), ordonnee(ev)
                    if 50 <= x <= 180 and 180 <= y <= 230:  # Reprendre
                        ferme_fenetre()
                        score, niveau, vitesse, grille = lecture_fichier_sauvegarde()
                        demarrer_jeu_sauvegarde(list(POLYOMINOS_STANDARDS.values()), score, niveau, vitesse, grille)

# Chaque pièce est une liste de listes représentant des blocs (1 pour un bloc, 0 pour un vide).
                        return
                    elif 220 <= x <= 350 and 180 <= y <= 230:  # Nouvelle Partie
                        ferme_fenetre()
                        initialiser_fenetre()
                        demarrer_jeu(list(POLYOMINOS_STANDARDS.values()), sauvegarde_possible=True)

# La aussi chaque pièce est une liste de listes représentant des blocs (1 pour un bloc, 0 pour un vide).
                        return
        else:
            initialiser_fenetre()
            demarrer_jeu(list(POLYOMINOS_STANDARDS.values()), sauvegarde_possible=True)

    elif mode == "polyominos":
        initialiser_fenetre()
        polyominos = lire_polyominos_corrige("polyominos.txt")
        demarrer_jeu(polyominos)
    elif mode == "pourrissement":
        initialiser_fenetre()
        demarrer_jeu(list(POLYOMINOS_STANDARDS.values()), mode="pourrissement")

    elif mode == "ia":
        initialiser_fenetre()
        jouer_ia(list(POLYOMINOS_STANDARDS.values()))


def evaluer_position(piece, pos_x, pos_y, grille):
    """Évalue une position possible pour une pièce."""
    # Simuler la grille avec la pièce placée
    grille_simulee = [ligne[:] for ligne in grille]
    for i, ligne in enumerate(piece):
        for j, cellule in enumerate(ligne):
            if cellule == 1:
                grille_simulee[pos_y + i][pos_x + j] = (1, "simule")

    # Critères d'évaluation
    lignes_completees = 0
    trous = 0
    hauteur_totale = 0
    rugosite = 0  # Variation entre les hauteurs des colonnes

    # Calculer le nombre de lignes complètes
    for ligne in grille_simulee:
        if all(cell[0] == 1 for cell in ligne):
            lignes_completees += 1

    # Calculer les trous et la hauteur des colonnes
    hauteurs = [0] * NB_COLONNES
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
    for x in range(NB_COLONNES):

        bloc_rencontre = False
        for y in range(NB_LIGNES):
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
            if grille_simulee[y][x][0] == 1:
                if not bloc_rencontre:
                    hauteurs[x] = NB_LIGNES - y

                    bloc_rencontre = True
            elif bloc_rencontre:
                trous += 1

    # Calculer la rugosité (différences de hauteurs entre colonnes adjacentes)
    for x in range(NB_COLONNES - 1):
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
        rugosite += abs(hauteurs[x] - hauteurs[x + 1])

    # Calculer la hauteur maximale
    hauteur_totale = max(hauteurs)

    # Calculer le score : prioriser les lignes complétées et minimiser les autres critères
    score = (
        lignes_completees * 1000   # Priorité majeure pour les lignes complètes
        - trous * 50               # Pénalisation pour les trous
        - hauteur_totale * 10      # Pénalisation pour la hauteur maximale
        - rugosite * 5             # Pénalisation pour une surface irrégulière
    )
    return score




def trouver_meilleure_position(piece, grille):
    """Trouve la meilleure position pour une pièce."""
    meilleur_score = float('-inf')
    meilleure_position = None

    # Tester toutes les rotations
    for _ in range(4):
        piece = rotation(piece)
        for pos_x in range(NB_COLONNES - len(piece[0]) + 1):
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
            pos_y = 0
            while verifier_position(piece, pos_x, pos_y + 1, grille):
                pos_y += 1
            
            # Évaluer la position
            score = evaluer_position(piece, pos_x, pos_y, grille)
            if score > meilleur_score:
                meilleur_score = score
                meilleure_position = (piece, pos_x, pos_y)

    return meilleure_position





def jouer_ia(polyominos):
    """Mode IA : L'ordinateur joue automatiquement avec animation de la chute et du déplacement des pièces."""
    grille_jeu = [[(0, None)] * NB_COLONNES for _ in range(NB_LIGNES)]
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
    score_actuel = 0
    niveau = 1
    vitesse = 0.5

    while True:
        piece_active, couleur_active = random.choice(polyominos), random.choice(COULEURS_BLOCS)
# Une liste contenant les couleurs des blocs du jeu. Chaque bloc sera affiché avec l'une d'elles.

        # Trouver la meilleure position pour la pièce
        meilleure_position = trouver_meilleure_position(piece_active, grille_jeu)
        if meilleure_position is None:
            # Si aucune position valide n'est trouvée, afficher Game Over
            afficher_game_over(score_actuel, niveau, sauvegarde_possible=False)
            return

        meilleure_piece, meilleur_x, meilleur_y = meilleure_position

        # Animation : déplacer horizontalement la pièce
        pos_x = NB_COLONNES // 2 - len(piece_active[0]) // 2
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
        pos_y = 0
        while pos_x != meilleur_x:
            if pos_x < meilleur_x:
                pos_x += 1
            elif pos_x > meilleur_x:
                pos_x -= 1

            # Mise à jour de l'affichage pour le déplacement horizontal
            efface_tout()
            dessiner_grille(grille_jeu)
            dessiner_bloc(piece_active, couleur_active, pos_x, pos_y)
            texte(10, 10, f"Score: {score_actuel}", taille=18, couleur="black")
            texte(10, 40, f"Niveau: {niveau}", taille=18, couleur="black")
            mise_a_jour()
            time.sleep(0.1)  # Pause pour ralentir le déplacement horizontal

        # Animation : faire tomber la pièce verticalement
        while pos_y < meilleur_y:
            pos_y += 1

            # Mise à jour de l'affichage pour la chute verticale
            efface_tout()
            dessiner_grille(grille_jeu)
            dessiner_bloc(piece_active, couleur_active, pos_x, pos_y)
            texte(10, 10, f"Score: {score_actuel}", taille=18, couleur="black")
            texte(10, 40, f"Niveau: {niveau}", taille=18, couleur="black")
            mise_a_jour()
            time.sleep(0.05)  # Pause pour ralentir la chute

        # Placer la pièce dans sa position finale
        piece_active = meilleure_piece
        for i, ligne in enumerate(piece_active):
            for j, cellule in enumerate(ligne):
                if cellule == 1:
                    grille_jeu[meilleur_y + i][meilleur_x + j] = (1, couleur_active)

        # Suppression des lignes complètes
        grille_jeu, lignes_supprimees = supprimer_lignes(grille_jeu)
        score_actuel += calculer_points(lignes_supprimees, niveau)

        # Progression de niveau et ajustement de la vitesse
        seuil_points = niveau * 500  # Le seuil de points pour atteindre le prochain niveau
        if score_actuel >= seuil_points:
            niveau += 1

            # Augmentation de la vitesse selon le niveau
            if niveau <= 5:
                # Progression modérée pour les premiers niveaux
                vitesse = max(0.2, 0.5 - (niveau - 1) * 0.05)
            else:
                # Progression rapide à partir du niveau 5
                vitesse = max(0.1, vitesse * 0.8)  # Réduction plus rapide du délai

        # Vérifier si la grille atteint le sommet
        if any(grille_jeu[0][x][0] == 1 for x in range(NB_COLONNES)):
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
            afficher_game_over(score_actuel, niveau, sauvegarde_possible=False)
            return

        # Mise à jour de l'affichage après chaque placement
        efface_tout()
        dessiner_grille(grille_jeu)
        texte(10, 10, f"Score: {score_actuel}", taille=18, couleur="black")
        texte(10, 40, f"Niveau: {niveau}", taille=18, couleur="black")
        mise_a_jour()
        time.sleep(vitesse)  # Pause pour ralentir l'IA

 



def calculer_score_ia(grille):
    """Calcule un score basé sur la qualité de la grille."""
    score = 0
    hauteur_totale = 0
    trous = 0

    for x in range(NB_COLONNES):
# NB_COLONNES et NB_LIGNES définissent la taille de la grille de jeu.
# Plus elles sont grandes, plus le terrain de jeu est vaste.
        colonne_hauteur = 0
        trou_colonne = False
        for y in range(NB_LIGNES):

            if grille[y][x][0] == 1:
                colonne_hauteur = NB_LIGNES - y

                if trou_colonne:
                    trous += 1
            elif colonne_hauteur > 0:
                trou_colonne = True

        hauteur_totale += colonne_hauteur

    # Pénalisation des trous, récompense pour une faible hauteur
    score -= trous * 5
    score -= hauteur_totale
    return score

if __name__ == "__main__":
    main()



