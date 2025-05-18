#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bibliothèque FLTK - Wrapper pour Tkinter
Fournit des fonctions simplifiées pour l'interface graphique
Adapté pour les projets de mini-jeux
"""

import tkinter as tk
from tkinter import filedialog, font
import time
import subprocess
import sys
import os
from collections import deque
from math import sqrt

__all__ = [
    # gestion de fenêtre
    'cree_fenetre', 'ferme_fenetre', 'mise_a_jour',
    # dessin
    'ligne', 'fleche', 'polygone', 'rectangle', 'cercle', 'point', 'image',
    'texte', 'taille_texte',
    # effacer
    'efface_tout', 'efface',
    # utilitaires
    'attente', 'capture_ecran', 'touche_pressee', 'abscisse_souris',
    'ordonnee_souris', 'donne_ev', 'attend_ev', 'attend_clic_gauche',
    'attend_fermeture', 'type_ev', 'abscisse', 'ordonnee', 'touche'
]


class CustomCanvas:
    """
    Classe qui encapsule tous les objets tkinter nécessaires à la création
    d'un canevas.
    """

    def __init__(self, width, height):
        # Création de la fenêtre principale
        self.root = tk.Tk()
        self.root.title("FLTK")
        self.root.protocol("WM_DELETE_WINDOW", self.ferme_fenetre)
        
        # Création du canevas principal
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self.root, width=width, height=height, 
                               highlightthickness=0, background="white")
        self.canvas.pack()
        
        # Dictionnaire pour référencer les objets créés
        self.objets = {}
        self.objets_efface = set()
        
        # Initialisation des événements
        self.ev_queue = deque()
        self.pressed_keys = set()
        self.canvas.bind("<Button-1>", self._clic_handler)
        self.canvas.bind("<ButtonRelease-1>", self._release_handler)
        self.canvas.bind("<Motion>", self._motion_handler)
        self.canvas.bind("<KeyPress>", self._key_press_handler)
        self.canvas.bind("<KeyRelease>", self._key_release_handler)
        self.canvas.focus_set()
        
        # Pour le suivi de la souris
        self.mouse_x = 0
        self.mouse_y = 0
        
        # Pour le suivi du temps
        self.time = time.time()

    def ferme_fenetre(self):
        """Ferme la fenêtre."""
        self.root.destroy()
        
    def _clic_handler(self, event):
        self.ev_queue.append(("ClicGauche", event))
        self.mouse_x = event.x
        self.mouse_y = event.y
        
    def _release_handler(self, event):
        self.ev_queue.append(("RelachementClicGauche", event))
        
    def _motion_handler(self, event):
        self.ev_queue.append(("Deplacement", event))
        self.mouse_x = event.x
        self.mouse_y = event.y
        
    def _key_press_handler(self, event):
        self.ev_queue.append(("Touche", event))
        self.pressed_keys.add(event.keysym)
        
    def _key_release_handler(self, event):
        self.ev_queue.append(("RelachementTouche", event))
        self.pressed_keys.discard(event.keysym)


# Initialisation de la fenêtre et du canevas
__canevas = None
__img = dict()


# Fonctions de gestion de fenêtre

def cree_fenetre(largeur, hauteur):
    """
    Crée une fenêtre de dimensions largeur x hauteur pixels.
    """
    global __canevas
    if __canevas is not None:
        raise RuntimeError("La fenêtre a déjà été créée")
    __canevas = CustomCanvas(largeur, hauteur)


def ferme_fenetre():
    """
    Détruit la fenêtre.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    __canevas.ferme_fenetre()
    __canevas = None


def mise_a_jour():
    """
    Met à jour la fenêtre. Les dessins ne sont affichés qu'après 
    l'appel à cette fonction.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    __canevas.root.update()


# Fonctions de dessin

def ligne(ax, ay, bx, by, couleur='black', epaisseur=1, tag=''):
    """
    Trace une ligne du point (ax, ay) au point (bx, by).
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    ligne_id = __canevas.canvas.create_line(
        ax, ay, bx, by, fill=couleur, width=epaisseur, tag=tag)
    if tag:
        if tag not in __canevas.objets:
            __canevas.objets[tag] = []
        __canevas.objets[tag].append(ligne_id)
    return ligne_id


def fleche(ax, ay, bx, by, couleur='black', epaisseur=1, tag=''):
    """
    Trace une flèche du point (ax, ay) au point (bx, by).
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    fleche_id = __canevas.canvas.create_line(
        ax, ay, bx, by, fill=couleur, width=epaisseur, arrow='last', tag=tag)
    if tag:
        if tag not in __canevas.objets:
            __canevas.objets[tag] = []
        __canevas.objets[tag].append(fleche_id)
    return fleche_id


def polygone(points, couleur='black', remplissage='', 
             epaisseur=1, tag=''):
    """
    Trace un polygone dont les points sont donnés dans la liste points 
    sous la forme [(x1, y1), (x2, y2), ...].
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    flat_points = []
    for point in points:
        flat_points.extend(point)
    polygone_id = __canevas.canvas.create_polygon(
        flat_points, fill=remplissage, outline=couleur, width=epaisseur, tag=tag)
    if tag:
        if tag not in __canevas.objets:
            __canevas.objets[tag] = []
        __canevas.objets[tag].append(polygone_id)
    return polygone_id


def rectangle(ax, ay, bx, by, couleur='black', remplissage='', 
              epaisseur=1, tag=''):
    """
    Trace un rectangle dont les coins opposés sont aux points 
    (ax, ay) et (bx, by).
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    rectangle_id = __canevas.canvas.create_rectangle(
        ax, ay, bx, by, fill=remplissage, outline=couleur, width=epaisseur, tag=tag)
    if tag:
        if tag not in __canevas.objets:
            __canevas.objets[tag] = []
        __canevas.objets[tag].append(rectangle_id)
    return rectangle_id


def cercle(x, y, r, couleur='black', remplissage='', 
           epaisseur=1, tag=''):
    """
    Trace un cercle de centre (x, y) et de rayon r.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    cercle_id = __canevas.canvas.create_oval(
        x - r, y - r, x + r, y + r, fill=remplissage, 
        outline=couleur, width=epaisseur, tag=tag)
    if tag:
        if tag not in __canevas.objets:
            __canevas.objets[tag] = []
        __canevas.objets[tag].append(cercle_id)
    return cercle_id


def point(x, y, couleur='black', epaisseur=1, tag=''):
    """
    Trace un point aux coordonnées (x, y).
    """
    return cercle(x, y, epaisseur, couleur, couleur, tag=tag)


def image(x, y, fichier, ancrage='center', tag=''):
    """
    Affiche l'image contenue dans fichier aux coordonnées (x, y).
    """
    global __canevas, __img
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    
    if fichier not in __img:
        __img[fichier] = tk.PhotoImage(file=fichier)
    
    img_id = __canevas.canvas.create_image(
        x, y, anchor=ancrage, image=__img[fichier], tag=tag)
    if tag:
        if tag not in __canevas.objets:
            __canevas.objets[tag] = []
        __canevas.objets[tag].append(img_id)
    return img_id


def texte(x, y, chaine, couleur='black', ancrage='nw', 
          police='Helvetica', taille=24, tag=''):
    """
    Affiche la chaîne de caractères chaine aux coordonnées (x, y).
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    text_font = font.Font(family=police, size=taille)
    text_id = __canevas.canvas.create_text(
        x, y, text=chaine, fill=couleur, font=text_font, anchor=ancrage, tag=tag)
    if tag:
        if tag not in __canevas.objets:
            __canevas.objets[tag] = []
        __canevas.objets[tag].append(text_id)
    return text_id


def taille_texte(chaine, police='Helvetica', taille=24):
    """
    Donne la largeur et la hauteur en pixels nécessaires pour afficher
    chaine avec la police et la taille données.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    text_font = font.Font(family=police, size=taille)
    return (text_font.measure(chaine), text_font.metrics("linespace"))


# Fonctions d'effacement

def efface_tout():
    """
    Efface tout le contenu de la fenêtre.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    __canevas.canvas.delete("all")
    __canevas.objets.clear()


def efface(objet):
    """
    Efface l'objet donné ou les objets du groupe donné.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    
    if isinstance(objet, int):
        __canevas.canvas.delete(objet)
        for tag, objets in __canevas.objets.items():
            if objet in objets:
                objets.remove(objet)
    elif isinstance(objet, str):
        __canevas.canvas.delete(objet)
        if objet in __canevas.objets:
            del __canevas.objets[objet]
    else:
        raise TypeError("Argument invalide")


# Fonctions utilitaires

def attente(temps):
    """
    Fait une pause de temps secondes.
    """
    start = time.time()
    while time.time() - start < temps:
        mise_a_jour()


def capture_ecran(file):
    """
    Fait une capture d'écran sauvegardée dans file.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    
    # Utilisation de la méthode postscript de tkinter
    __canevas.canvas.postscript(file=file + ".ps", colormode="color")
    
    # Conversion en PNG si ImageMagick est installé
    if sys.platform.startswith("win"):
        subprocess.call(["convert", file + ".ps", file + ".png"])
    else:
        os.system("convert " + file + ".ps " + file + ".png")
    
    # Suppression du fichier PS
    os.remove(file + ".ps")


def touche_pressee(touche):
    """
    Renvoie True si la touche est actuellement pressée.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    return touche in __canevas.pressed_keys


def abscisse_souris():
    """
    Renvoie l'abscisse de la souris.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    return __canevas.mouse_x


def ordonnee_souris():
    """
    Renvoie l'ordonnée de la souris.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    return __canevas.mouse_y


def donne_ev():
    """
    Renvoie le premier événement de la file d'attente,
    ou None si la file est vide.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    if not __canevas.ev_queue:
        return None
    return __canevas.ev_queue.popleft()


def attend_ev():
    """
    Attend qu'un événement arrive et le renvoie.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    while not __canevas.ev_queue:
        mise_a_jour()
    return __canevas.ev_queue.popleft()


def attend_clic_gauche():
    """
    Attend que l'utilisateur clique avec le bouton gauche et
    renvoie les coordonnées du clic.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    while True:
        ev = attend_ev()
        if type_ev(ev) == "ClicGauche":
            return (abscisse(ev), ordonnee(ev))


def attend_fermeture():
    """
    Attend que la fenêtre soit fermée par l'utilisateur.
    """
    global __canevas
    if __canevas is None:
        raise RuntimeError("La fenêtre n'a pas été créée")
    while __canevas is not None:
        mise_a_jour()


def type_ev(ev):
    """
    Renvoie une chaîne indiquant le type de l'événement.
    """
    return ev[0]


def abscisse(ev):
    """
    Renvoie l'abscisse associée à l'événement ev.
    """
    return ev[1].x


def ordonnee(ev):
    """
    Renvoie l'ordonnée associée à l'événement ev.
    """
    return ev[1].y


def touche(ev):
    """
    Renvoie la touche associée à l'événement ev.
    """
    return ev[1].keysym


if __name__ == "__main__":
    # Test de la bibliothèque
    cree_fenetre(600, 400)
    rectangle(100, 100, 500, 300, couleur='blue', remplissage='cyan')
    texte(300, 50, "Test de la bibliothèque FLTK", couleur='red', taille=24)
    cercle(300, 200, 50, couleur='green', remplissage='lime')
    ligne(100, 100, 500, 300, couleur='purple', epaisseur=3)
    attend_fermeture()
