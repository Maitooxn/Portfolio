// Description de mon implémentation Python du jeu Reversi

/*
Pour la version Python de Reversi (également connu sous le nom d'Othello), j'ai développé une 
implémentation complète utilisant Pygame pour l'interface graphique et un algorithme Minimax 
avec élagage alpha-beta pour l'intelligence artificielle.

Structure du code :
-----------------
1. Une classe principale ReversiGame qui gère la logique globale du jeu
2. Une classe Board pour représenter le plateau et gérer les règles du jeu
3. Une classe AI qui implémente l'algorithme Minimax pour l'intelligence artificielle
4. Une classe Disc pour gérer l'affichage et l'animation des pions
5. Une classe UIManager pour gérer l'interface utilisateur

Fonctionnalités implémentées :
---------------------------
- Plateau de jeu 8x8 avec interface graphique intuitive
- Mode joueur contre joueur et joueur contre IA
- Trois niveaux de difficulté pour l'IA (facile, moyen, difficile)
- Mise en évidence des coups légaux possibles
- Animation de retournement des pions
- Système de score en temps réel
- Détection automatique de fin de partie
- Possibilité de rejouer une partie

Algorithmes clés :
---------------
1. Algorithme Minimax avec élagage alpha-beta : Cet algorithme permet à l'IA d'évaluer les 
   différentes possibilités de jeu et de choisir le meilleur coup. L'élagage alpha-beta 
   optimise considérablement les performances en évitant d'explorer les branches inutiles.

   ```python
   def minimax(self, board, depth, alpha, beta, maximizing_player):
       # Cas de base : profondeur atteinte ou fin de partie
       if depth == 0 or board.is_game_over():
           return self.evaluate_board(board)
       
       valid_moves = board.get_valid_moves(maximizing_player)
       
       # Si aucun coup valide, passer le tour
       if not valid_moves:
           return self.minimax(board, depth - 1, alpha, beta, not maximizing_player)
       
       if maximizing_player:
           max_eval = float('-inf')
           for move in valid_moves:
               # Simuler le coup
               board_copy = board.copy()
               board_copy.make_move(move[0], move[1], True)
               
               # Évaluer récursivement
               eval = self.minimax(board_copy, depth - 1, alpha, beta, False)
               max_eval = max(max_eval, eval)
               
               # Élagage alpha
               alpha = max(alpha, eval)
               if beta <= alpha:
                   break
                   
           return max_eval
       else:
           min_eval = float('inf')
           for move in valid_moves:
               # Simuler le coup
               board_copy = board.copy()
               board_copy.make_move(move[0], move[1], False)
               
               # Évaluer récursivement
               eval = self.minimax(board_copy, depth - 1, alpha, beta, True)
               min_eval = min(min_eval, eval)
               
               # Élagage beta
               beta = min(beta, eval)
               if beta <= alpha:
                   break
                   
           return min_eval
   ```

2. Fonction d'évaluation du plateau : J'ai implémenté une fonction d'évaluation sophistiquée 
   qui prend en compte plusieurs facteurs :
   - Le nombre de pions de chaque joueur
   - La valeur stratégique des cases occupées (coins, bords, etc.)
   - La mobilité (nombre de coups possibles)
   - La parité (avantage au dernier joueur à jouer)

3. Détection des coups valides : Algorithme qui vérifie dans toutes les directions si un coup 
   est légal selon les règles du Reversi.

Défis techniques surmontés :
-------------------------
- Optimisation de l'algorithme Minimax pour permettre une profondeur de recherche suffisante
- Création d'une IA avec différents niveaux de difficulté adaptés aux joueurs
- Implémentation d'animations fluides pour le retournement des pions
- Gestion des situations spéciales (passage de tour, fin de partie)

Pour jouer à ma version Python de Reversi, vous aurez besoin d'installer :
- Python 3.6 ou supérieur
- Pygame (pip install pygame)

Lancez ensuite le jeu avec la commande : python reversi.py
*/
