import pygame
import random
import sys
from pygame.locals import *

"""
Jeu Tetris en Python avec Pygame
Développé par Jordan Oshoffa
"""

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH * BLOCK_SIZE) // 2
BOARD_Y = SCREEN_HEIGHT - (BOARD_HEIGHT * BLOCK_SIZE) - 50

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

# Formes des pièces
SHAPES = [
    # I
    [
        ['.....',
         '.....',
         'IIII.',
         '.....',
         '.....'],
        ['..I..',
         '..I..',
         '..I..',
         '..I..',
         '.....']
    ],
    # J
    [
        ['.....',
         '.J...',
         '.JJJ.',
         '.....',
         '.....'],
        ['.....',
         '..JJ.',
         '..J..',
         '..J..',
         '.....'],
        ['.....',
         '.....',
         '.JJJ.',
         '...J.',
         '.....'],
        ['.....',
         '..J..',
         '..J..',
         '.JJ..',
         '.....']
    ],
    # L
    [
        ['.....',
         '...L.',
         '.LLL.',
         '.....',
         '.....'],
        ['.....',
         '..L..',
         '..L..',
         '..LL.',
         '.....'],
        ['.....',
         '.....',
         '.LLL.',
         '.L...',
         '.....'],
        ['.....',
         '.LL..',
         '..L..',
         '..L..',
         '.....']
    ],
    # O
    [
        ['.....',
         '.....',
         '.OO..',
         '.OO..',
         '.....']
    ],
    # S
    [
        ['.....',
         '.....',
         '..SS.',
         '.SS..',
         '.....'],
        ['.....',
         '..S..',
         '..SS.',
         '...S.',
         '.....']
    ],
    # T
    [
        ['.....',
         '..T..',
         '.TTT.',
         '.....',
         '.....'],
        ['.....',
         '..T..',
         '..TT.',
         '..T..',
         '.....'],
        ['.....',
         '.....',
         '.TTT.',
         '..T..',
         '.....'],
        ['.....',
         '..T..',
         '.TT..',
         '..T..',
         '.....']
    ],
    # Z
    [
        ['.....',
         '.....',
         '.ZZ..',
         '..ZZ.',
         '.....'],
        ['.....',
         '...Z.',
         '..ZZ.',
         '..Z..',
         '.....']
    ]
]

# Couleurs des pièces
SHAPE_COLORS = [
    CYAN,    # I
    BLUE,    # J
    ORANGE,  # L
    YELLOW,  # O
    GREEN,   # S
    PURPLE,  # T
    RED      # Z
]

class Tetromino:
    def __init__(self, x, y, shape_idx):
        self.x = x
        self.y = y
        self.shape_idx = shape_idx
        self.rotation = 0
        self.shape = SHAPES[shape_idx]
        self.color = SHAPE_COLORS[shape_idx]
    
    def get_shape(self):
        return self.shape[self.rotation]
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)
    
    def rotate_back(self):
        self.rotation = (self.rotation - 1) % len(self.shape)

class TetrisGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tetris - Jordan Oshoffa")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 48)
        
        self.reset_game()
    
    def reset_game(self):
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False
        self.paused = False
        self.fall_time = 0
        self.fall_speed = 0.5  # Secondes
    
    def new_piece(self):
        # Créer une nouvelle pièce aléatoire
        shape_idx = random.randint(0, len(SHAPES) - 1)
        return Tetromino(BOARD_WIDTH // 2 - 2, 0, shape_idx)
    
    def valid_position(self, piece, x_offset=0, y_offset=0):
        # Vérifier si la position est valide
        for y, row in enumerate(piece.get_shape()):
            for x, cell in enumerate(row):
                if cell == '.':
                    continue
                
                pos_x = piece.x + x + x_offset
                pos_y = piece.y + y + y_offset
                
                if (pos_x < 0 or pos_x >= BOARD_WIDTH or 
                    pos_y >= BOARD_HEIGHT or 
                    (pos_y >= 0 and self.board[pos_y][pos_x] != 0)):
                    return False
        return True
    
    def add_to_board(self, piece):
        # Ajouter la pièce au plateau
        for y, row in enumerate(piece.get_shape()):
            for x, cell in enumerate(row):
                if cell != '.':
                    self.board[piece.y + y][piece.x + x] = piece.color
    
    def clear_lines(self):
        # Effacer les lignes complètes et calculer le score
        lines_cleared = 0
        y = BOARD_HEIGHT - 1
        while y >= 0:
            if all(cell != 0 for cell in self.board[y]):
                # Ligne complète trouvée
                lines_cleared += 1
                
                # Déplacer toutes les lignes au-dessus vers le bas
                for y2 in range(y, 0, -1):
                    self.board[y2] = self.board[y2 - 1][:]
                
                # Effacer la ligne du haut
                self.board[0] = [0] * BOARD_WIDTH
            else:
                y -= 1
        
        # Mettre à jour le score et le niveau
        if lines_cleared > 0:
            points = {1: 40, 2: 100, 3: 300, 4: 1200}
            self.score += points.get(lines_cleared, 0) * self.level
            self.lines += lines_cleared
            self.level = self.lines // 10 + 1
            self.fall_speed = max(0.05, 0.5 - (self.level - 1) * 0.05)
        
        return lines_cleared
    
    def draw_board(self):
        # Dessiner le plateau de jeu
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x] != 0:
                    self.draw_block(BOARD_X + x * BLOCK_SIZE, 
                                   BOARD_Y + y * BLOCK_SIZE, 
                                   self.board[y][x])
        
        # Dessiner la bordure
        pygame.draw.rect(self.screen, WHITE, 
                         (BOARD_X, BOARD_Y, 
                          BOARD_WIDTH * BLOCK_SIZE, 
                          BOARD_HEIGHT * BLOCK_SIZE), 2)
        
        # Dessiner la grille
        for x in range(BOARD_WIDTH + 1):
            pygame.draw.line(self.screen, GRAY, 
                            (BOARD_X + x * BLOCK_SIZE, BOARD_Y), 
                            (BOARD_X + x * BLOCK_SIZE, BOARD_Y + BOARD_HEIGHT * BLOCK_SIZE))
        for y in range(BOARD_HEIGHT + 1):
            pygame.draw.line(self.screen, GRAY, 
                            (BOARD_X, BOARD_Y + y * BLOCK_SIZE), 
                            (BOARD_X + BOARD_WIDTH * BLOCK_SIZE, BOARD_Y + y * BLOCK_SIZE))
    
    def draw_piece(self, piece, offset_x=0, offset_y=0):
        # Dessiner une pièce
        shape = piece.get_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell != '.':
                    self.draw_block(BOARD_X + (piece.x + x) * BLOCK_SIZE + offset_x, 
                                   BOARD_Y + (piece.y + y) * BLOCK_SIZE + offset_y, 
                                   piece.color)
    
    def draw_next_piece(self):
        # Dessiner la prochaine pièce
        next_x = BOARD_X + BOARD_WIDTH * BLOCK_SIZE + 50
        next_y = BOARD_Y + 100
        
        # Cadre
        pygame.draw.rect(self.screen, WHITE, 
                         (next_x, next_y, 5 * BLOCK_SIZE, 5 * BLOCK_SIZE), 2)
        
        # Titre
        next_text = self.font.render("Suivant:", True, WHITE)
        self.screen.blit(next_text, (next_x, next_y - 40))
        
        # Pièce
        shape = self.next_piece.get_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell != '.':
                    self.draw_block(next_x + x * BLOCK_SIZE, 
                                   next_y + y * BLOCK_SIZE, 
                                   self.next_piece.color)
    
    def draw_info(self):
        # Dessiner les informations du jeu
        info_x = BOARD_X - 200
        info_y = BOARD_Y + 100
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (info_x, info_y))
        
        # Niveau
        level_text = self.font.render(f"Niveau: {self.level}", True, WHITE)
        self.screen.blit(level_text, (info_x, info_y + 40))
        
        # Lignes
        lines_text = self.font.render(f"Lignes: {self.lines}", True, WHITE)
        self.screen.blit(lines_text, (info_x, info_y + 80))
        
        # Contrôles
        controls_y = info_y + 150
        controls_text = self.font.render("Contrôles:", True, WHITE)
        self.screen.blit(controls_text, (info_x, controls_y))
        
        controls = [
            "← → : Déplacer",
            "↑ : Rotation",
            "↓ : Descente rapide",
            "Espace : Chute",
            "P : Pause"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.font.render(control, True, WHITE)
            self.screen.blit(control_text, (info_x, controls_y + 40 + i * 30))
    
    def draw_block(self, x, y, color):
        # Dessiner un bloc avec effet 3D
        pygame.draw.rect(self.screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.screen, WHITE, (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)
        
        # Effet 3D
        pygame.draw.polygon(self.screen, self.lighten_color(color), 
                           [(x, y), (x + BLOCK_SIZE, y), (x + BLOCK_SIZE - 4, y + 4), (x + 4, y + 4)])
        pygame.draw.polygon(self.screen, self.lighten_color(color), 
                           [(x, y), (x, y + BLOCK_SIZE), (x + 4, y + BLOCK_SIZE - 4), (x + 4, y + 4)])
        pygame.draw.polygon(self.screen, self.darken_color(color), 
                           [(x + BLOCK_SIZE, y), (x + BLOCK_SIZE, y + BLOCK_SIZE), 
                            (x + BLOCK_SIZE - 4, y + BLOCK_SIZE - 4), (x + BLOCK_SIZE - 4, y + 4)])
        pygame.draw.polygon(self.screen, self.darken_color(color), 
                           [(x, y + BLOCK_SIZE), (x + BLOCK_SIZE, y + BLOCK_SIZE), 
                            (x + BLOCK_SIZE - 4, y + BLOCK_SIZE - 4), (x + 4, y + BLOCK_SIZE - 4)])
    
    def lighten_color(self, color):
        # Éclaircir une couleur
        r, g, b = color
        return min(255, r + 50), min(255, g + 50), min(255, b + 50)
    
    def darken_color(self, color):
        # Assombrir une couleur
        r, g, b = color
        return max(0, r - 50), max(0, g - 50), max(0, b - 50)
    
    def draw_game_over(self):
        # Afficher l'écran de fin de jeu
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.big_font.render("GAME OVER", True, WHITE)
        score_text = self.font.render(f"Score final: {self.score}", True, WHITE)
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
    
    def draw_pause(self):
        # Afficher l'écran de pause
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.big_font.render("PAUSE", True, WHITE)
        continue_text = self.font.render("Appuyez sur P pour continuer", True, WHITE)
        
        self.screen.blit(pause_text, 
                        (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(continue_text, 
                        (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 + 30))
    
    def hard_drop(self):
        # Faire tomber la pièce instantanément
        drop_distance = 0
        while self.valid_position(self.current_piece, 0, drop_distance + 1):
            drop_distance += 1
        
        self.current_piece.y += drop_distance
        self.add_to_board(self.current_piece)
        self.score += drop_distance * 2  # Points bonus pour la chute instantanée
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        # Vérifier si le jeu est terminé
        if not self.valid_position(self.current_piece):
            self.game_over = True
    
    def run(self):
        # Boucle principale du jeu
        last_move_down_time = pygame.time.get_ticks()
        
        while True:
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - last_move_down_time) / 1000.0  # En secondes
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == KEYDOWN:
                    if event.key == K_r and self.game_over:
                        self.reset_game()
                    
                    if event.key == K_p:
                        self.paused = not self.paused
                    
                    if not self.paused and not self.game_over:
                        if event.key == K_LEFT:
                            if self.valid_position(self.current_piece, -1, 0):
                                self.current_piece.x -= 1
                        
                        elif event.key == K_RIGHT:
                            if self.valid_position(self.current_piece, 1, 0):
                                self.current_piece.x += 1
                        
                        elif event.key == K_DOWN:
                            if self.valid_position(self.current_piece, 0, 1):
                                self.current_piece.y += 1
                                self.score += 1  # Points bonus pour la descente rapide
                        
                        elif event.key == K_UP:
                            self.current_piece.rotate()
                            if not self.valid_position(self.current_piece):
                                self.current_piece.rotate_back()
                        
                        elif event.key == K_SPACE:
                            self.hard_drop()
            
            # Mise à jour du jeu
            if not self.paused and not self.game_over:
                # Descente automatique de la pièce
                if delta_time > self.fall_speed:
                    if self.valid_position(self.current_piece, 0, 1):
                        self.current_piece.y += 1
                    else:
                        # La pièce ne peut plus descendre
                        self.add_to_board(self.current_piece)
                        self.clear_lines()
                        self.current_piece = self.next_piece
                        self.next_piece = self.new_piece()
                        
                        # Vérifier si le jeu est terminé
                        if not self.valid_position(self.current_piece):
                            self.game_over = True
                    
                    last_move_down_time = current_time
            
            # Dessin
            self.screen.fill(BLACK)
            self.draw_board()
            
            if not self.game_over:
                self.draw_piece(self.current_piece)
            
            self.draw_next_piece()
            self.draw_info()
            
            if self.game_over:
                self.draw_game_over()
            
            if self.paused:
                self.draw_pause()
            
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = TetrisGame()
    game.run()
