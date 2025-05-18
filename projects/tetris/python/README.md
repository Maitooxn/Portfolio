// Description de mon implémentation Python du jeu Tetris

/*
Pour la version Python de Tetris, j'ai utilisé la bibliothèque Pygame qui est parfaitement adaptée 
au développement de jeux 2D. Voici comment j'ai structuré mon code et les principales fonctionnalités 
que j'ai implémentées :

Structure du code :
-----------------
1. Une classe principale TetrisGame qui gère la logique globale du jeu
2. Une classe Tetromino pour représenter les différentes pièces et leurs rotations
3. Une classe Board pour gérer la grille de jeu et les collisions
4. Une classe ScoreSystem pour la gestion du score et des niveaux

Fonctionnalités implémentées :
---------------------------
- Génération aléatoire des pièces avec leurs différentes formes
- Rotation des pièces avec vérification des collisions
- Déplacement latéral et accélération de la chute
- Détection et suppression des lignes complètes
- Système de score progressif (plus de points pour plusieurs lignes simultanées)
- Augmentation de la difficulté avec le niveau
- Affichage de la pièce suivante
- Système de pause et de game over

Algorithmes clés :
---------------
1. Rotation des pièces : J'ai utilisé une matrice de transformation pour faire pivoter les pièces
   tout en vérifiant que la nouvelle position est valide.

2. Détection des collisions : Vérification de chaque cellule de la pièce par rapport aux limites
   du plateau et aux autres pièces déjà placées.

3. Suppression des lignes : Parcours du plateau pour identifier les lignes complètes, puis
   décalage des lignes supérieures vers le bas.

Défis techniques surmontés :
-------------------------
- Gestion des collisions lors des rotations près des bords
- Implémentation d'un système de "wall kick" pour permettre certaines rotations
- Optimisation de la boucle de jeu pour maintenir une fluidité constante
- Création d'effets visuels pour la suppression des lignes

Pour jouer à ma version Python de Tetris, vous aurez besoin d'installer :
- Python 3.6 ou supérieur
- Pygame (pip install pygame)

Lancez ensuite le jeu avec la commande : python tetris.py
*/
