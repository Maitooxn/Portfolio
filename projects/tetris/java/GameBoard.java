package tetris;

import java.util.List;

/**
 * Classe représentant le plateau de jeu Tetris
 * Gère la grille de jeu, les collisions et la suppression des lignes
 * @author Jordan Oshoffa
 */
public class GameBoard {
    private int width;
    private int height;
    private int[][] grid;
    
    /**
     * Constructeur initialisant un plateau vide
     */
    public GameBoard(int width, int height) {
        this.width = width;
        this.height = height;
        this.grid = new int[height][width];
        
        // Initialiser la grille avec des zéros (cases vides)
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                grid[y][x] = 0;
            }
        }
    }
    
    /**
     * Vérifie si une position est valide pour une pièce
     */
    public boolean isValidPosition(Tetromino piece) {
        List<int[]> blockPositions = piece.getBlockPositions();
        
        for (int[] pos : blockPositions) {
            int x = pos[0];
            int y = pos[1];
            
            // Vérifier les limites du plateau
            if (x < 0 || x >= width || y < 0 || y >= height) {
                return false;
            }
            
            // Vérifier les collisions avec les blocs existants
            if (y >= 0 && grid[y][x] != 0) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * Place une pièce sur le plateau
     */
    public void placePiece(Tetromino piece) {
        List<int[]> blockPositions = piece.getBlockPositions();
        
        for (int[] pos : blockPositions) {
            int x = pos[0];
            int y = pos[1];
            
            if (y >= 0 && y < height && x >= 0 && x < width) {
                grid[y][x] = piece.getColorCode();
            }
        }
    }
    
    /**
     * Vérifie et supprime les lignes complètes
     * @return Le nombre de lignes supprimées
     */
    public int clearLines() {
        int linesCleared = 0;
        
        for (int y = height - 1; y >= 0; y--) {
            boolean lineIsFull = true;
            
            // Vérifier si la ligne est complète
            for (int x = 0; x < width; x++) {
                if (grid[y][x] == 0) {
                    lineIsFull = false;
                    break;
                }
            }
            
            if (lineIsFull) {
                // Supprimer la ligne et faire descendre les lignes au-dessus
                linesCleared++;
                
                // Déplacer toutes les lignes au-dessus vers le bas
                for (int y2 = y; y2 > 0; y2--) {
                    for (int x = 0; x < width; x++) {
                        grid[y2][x] = grid[y2 - 1][x];
                    }
                }
                
                // Effacer la ligne du haut
                for (int x = 0; x < width; x++) {
                    grid[0][x] = 0;
                }
                
                // Vérifier à nouveau la même ligne (qui contient maintenant les blocs descendus)
                y++;
            }
        }
        
        return linesCleared;
    }
    
    /**
     * Vérifie si le jeu est terminé (blocs atteignant le haut)
     */
    public boolean isGameOver() {
        // Vérifier si des blocs sont présents dans la ligne du haut
        for (int x = 0; x < width; x++) {
            if (grid[0][x] != 0) {
                return true;
            }
        }
        return false;
    }
    
    /**
     * Réinitialise le plateau
     */
    public void reset() {
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                grid[y][x] = 0;
            }
        }
    }
    
    // Getters
    
    public int[][] getGrid() {
        return grid;
    }
    
    public int getWidth() {
        return width;
    }
    
    public int getHeight() {
        return height;
    }
}
