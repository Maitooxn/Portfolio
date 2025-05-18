import pygame
import random
import sys
from pygame.locals import *
from collections import deque
import heapq

"""
Jeu ColorLines en Python avec Pygame
Développé par Jordan Oshoffa
"""

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
CELL_SIZE = 50
BOARD_SIZE = 9
BOARD_X = (SCREEN_WIDTH - BOARD_SIZE * CELL_SIZE) // 2
BOARD_Y = 50
NEW_BALLS_PER_TURN = 3
MIN_LINE_LENGTH = 5

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Couleurs des billes
BALL_COLORS = [RED, BLUE, GREEN, YELLOW, PURPLE, CYAN, ORANGE]

class Ball:
    def __init__(self, color_index):
        self.color_index = color_index
        self.color = BALL_COLORS[color_index]

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
    
    def get_ball(self, x, y):
        if self.is_valid_position(x, y):
            return self.grid[y][x]
        return None
    
    def set_ball(self, x, y, ball):
        if self.is_valid_position(x, y):
            self.grid[y][x] = ball
    
    def is_valid_position(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size
    
    def is_empty(self, x, y):
        return self.is_valid_position(x, y) and self.grid[y][x] is None
    
    def is_full(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] is None:
                    return False
        return True
    
    def clear(self):
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x] = None
    
    def find_lines(self, min_length):
        lines = []
        
        # Vérifier les lignes horizontales
        for y in range(self.size):
            for x in range(self.size - min_length + 1):
                if self.grid[y][x] is not None:
                    length = 1
                    color_index = self.grid[y][x].color_index
                    
                    for i in range(1, self.size - x):
                        if (self.grid[y][x + i] is not None and 
                            self.grid[y][x + i].color_index == color_index):
                            length += 1
                        else:
                            break
                    
                    if length >= min_length:
                        lines.append([(x + i, y) for i in range(length)])
                        x += length - 1  # Sauter les positions déjà vérifiées
        
        # Vérifier les lignes verticales
        for x in range(self.size):
            for y in range(self.size - min_length + 1):
                if self.grid[y][x] is not None:
                    length = 1
                    color_index = self.grid[y][x].color_index
                    
                    for i in range(1, self.size - y):
                        if (self.grid[y + i][x] is not None and 
                            self.grid[y + i][x].color_index == color_index):
                            length += 1
                        else:
                            break
                    
                    if length >= min_length:
                        lines.append([(x, y + i) for i in range(length)])
                        y += length - 1  # Sauter les positions déjà vérifiées
        
        # Vérifier les diagonales (haut-gauche à bas-droite)
        for y in range(self.size - min_length + 1):
            for x in range(self.size - min_length + 1):
                if self.grid[y][x] is not None:
                    length = 1
                    color_index = self.grid[y][x].color_index
                    
                    for i in range(1, min(self.size - x, self.size - y)):
                        if (self.grid[y + i][x + i] is not None and 
                            self.grid[y + i][x + i].color_index == color_index):
                            length += 1
                        else:
                            break
                    
                    if length >= min_length:
                        lines.append([(x + i, y + i) for i in range(length)])
        
        # Vérifier les diagonales (haut-droite à bas-gauche)
        for y in range(self.size - min_length + 1):
            for x in range(min_length - 1, self.size):
                if self.grid[y][x] is not None:
                    length = 1
                    color_index = self.grid[y][x].color_index
                    
                    for i in range(1, min(x + 1, self.size - y)):
                        if (self.grid[y + i][x - i] is not None and 
                            self.grid[y + i][x - i].color_index == color_index):
                            length += 1
                        else:
                            break
                    
                    if length >= min_length:
                        lines.append([(x - i, y + i) for i in range(length)])
        
        return lines
    
    def has_lines(self, min_length):
        return len(self.find_lines(min_length)) > 0

class AStar:
    def __init__(self, board):
        self.board = board
    
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def get_neighbors(self, point):
        x, y = point
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Bas, Droite, Haut, Gauche
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.board.is_valid_position(nx, ny) and self.board.is_empty(nx, ny):
                neighbors.append((nx, ny))
        
        return neighbors
    
    def find_path(self, start, end):
        # Si la destination est occupée, pas de chemin possible
        if not self.board.is_empty(*end):
            return None
        
        # Initialisation des structures pour A*
        open_set = []
        closed_set = set()
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}
        
        heapq.heappush(open_set, (f_score[start], start))
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == end:
                # Reconstruire le chemin
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path
            
            closed_set.add(current)
            
            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue
                
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end)
                    
                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        # Aucun chemin trouvé
        return None

class ScoreSystem:
    def __init__(self):
        self.score = 0
        self.high_score = self.load_high_score()
    
    def add_score(self, points):
        # Formule de score : points au carré * 10
        self.score += points * points * 10
    
    def reset_score(self):
        self.score = 0
    
    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
    
    def load_high_score(self):
        try:
            with open("colorlines_highscore.txt", "r") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
    
    def save_high_score(self):
        try:
            with open("colorlines_highscore.txt", "w") as file:
                file.write(str(self.high_score))
        except:
            pass

class ColorLinesGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("ColorLines - Jordan Oshoffa")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 48)
        
        self.board = Board(BOARD_SIZE)
        self.score_system = ScoreSystem()
        self.path_finder = AStar(self.board)
        
        self.selected_pos = None
        self.next_balls = []
        self.game_over = False
        
        self.start_new_game()
    
    def start_new_game(self):
        self.board.clear()
        self.score_system.reset_score()
        self.selected_pos = None
        self.next_balls = self.generate_next_balls()
        self.add_new_balls()
        self.game_over = False
    
    def generate_next_balls(self):
        return [Ball(random.randint(0, len(BALL_COLORS) - 1)) for _ in range(NEW_BALLS_PER_TURN)]
    
    def add_new_balls(self):
        if self.board.is_full():
            self.game_over = True
            return
        
        for ball in self.next_balls:
            x, y = self.get_random_empty_cell()
            self.board.set_ball(x, y, ball)
        
        # Vérifier les alignements après avoir ajouté les nouvelles billes
        self.check_lines()
        
        # Générer les prochaines billes
        self.next_balls = self.generate_next_balls()
        
        # Vérifier si le plateau est plein
        if self.board.is_full():
            self.game_over = True
            self.score_system.update_high_score()
    
    def get_random_empty_cell(self):
        empty_cells = []
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.is_empty(x, y):
                    empty_cells.append((x, y))
        
        return random.choice(empty_cells)
    
    def check_lines(self):
        lines = self.board.find_lines(MIN_LINE_LENGTH)
        if lines:
            total_balls = 0
            
            for line in lines:
                total_balls += len(line)
                
                # Supprimer les billes de la ligne
                for x, y in line:
                    self.board.set_ball(x, y, None)
            
            # Mettre à jour le score
            self.score_system.add_score(total_balls)
            return True
        
        return False
    
    def handle_click(self, pos):
        if self.game_over:
            return
        
        # Convertir les coordonnées de l'écran en coordonnées de la grille
        x = (pos[0] - BOARD_X) // CELL_SIZE
        y = (pos[1] - BOARD_Y) // CELL_SIZE
        
        if not self.board.is_valid_position(x, y):
            return
        
        if self.selected_pos is None:
            # Aucune bille sélectionnée, essayer d'en sélectionner une
            if self.board.get_ball(x, y) is not None:
                self.selected_pos = (x, y)
        else:
            # Une bille est déjà sélectionnée
            if (x, y) == self.selected_pos:
                # Désélectionner la bille
                self.selected_pos = None
            elif self.board.get_ball(x, y) is None:
                # Essayer de déplacer la bille vers une case vide
                path = self.path_finder.find_path(self.selected_pos, (x, y))
                
                if path:
                    # Déplacer la bille
                    ball = self.board.get_ball(*self.selected_pos)
                    self.board.set_ball(*self.selected_pos, None)
                    self.board.set_ball(x, y, ball)
                    
                    # Réinitialiser la sélection
                    self.selected_pos = None
                    
                    # Vérifier les alignements
                    if not self.check_lines():
                        # Ajouter de nouvelles billes si aucun alignement n'a été trouvé
                        self.add_new_balls()
            else:
                # Sélectionner une autre bille
                self.selected_pos = (x, y)
    
    def draw(self):
        # Fond d'écran
        self.screen.fill(BLACK)
        
        # Dessiner le plateau
        for y in range(self.board.size):
            for x in range(self.board.size):
                # Dessiner la case
                rect = pygame.Rect(BOARD_X + x * CELL_SIZE, BOARD_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GRAY, rect, 1)
                
                # Dessiner la bille si présente
                ball = self.board.get_ball(x, y)
                if ball:
                    self.draw_ball(x, y, ball.color, (x, y) == self.selected_pos)
        
        # Dessiner les informations
        score_text = self.font.render(f"Score: {self.score_system.score}", True, WHITE)
        high_score_text = self.font.render(f"Meilleur score: {self.score_system.high_score}", True, WHITE)
        next_text = self.font.render("Prochaines billes:", True, WHITE)
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(high_score_text, (20, 50))
        self.screen.blit(next_text, (SCREEN_WIDTH - 200, 20))
        
        # Dessiner les prochaines billes
        for i, ball in enumerate(self.next_balls):
            pygame.draw.circle(self.screen, ball.color, 
                              (SCREEN_WIDTH - 150 + i * 40, 50), 15)
        
        # Dessiner le message de fin de jeu
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.big_font.render("GAME OVER", True, WHITE)
            score_text = self.font.render(f"Score final: {self.score_system.score}", True, WHITE)
            restart_text = self.font.render("Appuyez sur R pour recommencer", True, WHITE)
            
            self.screen.blit(game_over_text, 
                            (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                             SCREEN_HEIGHT // 2 - 60))
            self.screen.blit(score_text, 
                            (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                             SCREEN_HEIGHT // 2))
            self.screen.blit(restart_text, 
                            (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                             SCREEN_HEIGHT // 2 + 60))
    
    def draw_ball(self, x, y, color, selected):
        center_x = BOARD_X + x * CELL_SIZE + CELL_SIZE // 2
        center_y = BOARD_Y + y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 5
        
        if selected:
            # Dessiner un halo autour de la bille sélectionnée
            pygame.draw.circle(self.screen, WHITE, (center_x, center_y), radius + 3)
        
        # Dessiner la bille
        pygame.draw.circle(self.screen, color, (center_x, center_y), radius)
        
        # Effet 3D (reflet)
        highlight_radius = radius // 3
        highlight_offset = radius // 3
        pygame.draw.circle(self.screen, self.lighten_color(color), 
                          (center_x - highlight_offset, center_y - highlight_offset), 
                          highlight_radius)
    
    def lighten_color(self, color):
        r, g, b = color
        return min(255, r + 100), min(255, g + 100), min(255, b + 100)
    
    def run(self):
        running = True
        
        while running:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        self.handle_click(event.pos)
                
                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        self.start_new_game()
            
            # Dessin
            self.draw()
            
            # Mise à jour de l'écran
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ColorLinesGame()
    game.run()
