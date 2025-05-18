// Description de mon implémentation Python du jeu ColorLines

/*
Pour la version Python de ColorLines, j'ai utilisé la bibliothèque Pygame pour créer une interface 
graphique interactive et fluide. Ce jeu de puzzle stratégique a nécessité l'implémentation d'un 
algorithme de pathfinding pour permettre aux billes de se déplacer intelligemment sur le plateau.

Structure du code :
-----------------
1. Une classe principale ColorLinesGame qui gère la logique globale du jeu
2. Une classe Ball pour représenter les billes colorées et leurs animations
3. Une classe Board pour gérer la grille de jeu et les interactions
4. Une classe PathFinder qui implémente l'algorithme A* pour trouver le chemin optimal
5. Une classe Point pour simplifier la gestion des coordonnées
6. Une classe ScoreManager pour gérer le score et les meilleurs scores

Fonctionnalités implémentées :
---------------------------
- Génération aléatoire de billes de différentes couleurs
- Sélection et déplacement des billes avec vérification de chemin
- Détection des alignements (horizontaux, verticaux et diagonaux)
- Suppression des alignements de 5 billes ou plus
- Système de score progressif (plus de points pour plus de billes alignées)
- Prédiction des prochaines billes à apparaître
- Sauvegarde des meilleurs scores

Algorithmes clés :
---------------
1. Algorithme A* pour le pathfinding : J'ai implémenté cet algorithme pour trouver le chemin 
   le plus court entre deux points du plateau, en évitant les obstacles (autres billes).
   
   ```python
   def find_path(self, start, end):
       # Initialisation des ensembles ouverts et fermés
       open_set = []
       closed_set = set()
       
       # Dictionnaires pour stocker les scores g et f, et les parents
       g_score = {start: 0}
       f_score = {start: self.heuristic(start, end)}
       came_from = {}
       
       heapq.heappush(open_set, (f_score[start], start))
       
       while open_set:
           # Récupérer le nœud avec le score f le plus bas
           current = heapq.heappop(open_set)[1]
           
           if current == end:
               # Reconstruire le chemin
               path = []
               while current in came_from:
                   path.append(current)
                   current = came_from[current]
               return path[::-1]  # Inverser pour avoir le chemin du début à la fin
           
           closed_set.add(current)
           
           # Explorer les voisins
           for neighbor in self.get_neighbors(current):
               if neighbor in closed_set:
                   continue
                   
               tentative_g_score = g_score[current] + 1
               
               if neighbor not in [i[1] for i in open_set] or tentative_g_score < g_score.get(neighbor, float('inf')):
                   came_from[neighbor] = current
                   g_score[neighbor] = tentative_g_score
                   f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end)
                   heapq.heappush(open_set, (f_score[neighbor], neighbor))
       
       return None  # Aucun chemin trouvé
   ```

2. Détection des alignements : Algorithme qui parcourt le plateau dans toutes les directions 
   pour trouver des séquences de billes de même couleur.

3. Gestion de la gravité : Après la suppression des alignements, les billes tombent pour remplir 
   les espaces vides.

Défis techniques surmontés :
-------------------------
- Implémentation efficace de l'algorithme A* pour garantir des déplacements fluides
- Gestion des animations lors des déplacements et des suppressions de billes
- Optimisation des performances pour gérer un grand nombre de billes et de mouvements
- Création d'une interface utilisateur intuitive et réactive

Pour jouer à ma version Python de ColorLines, vous aurez besoin d'installer :
- Python 3.6 ou supérieur
- Pygame (pip install pygame)

Lancez ensuite le jeu avec la commande : python colorlines.py
*/
