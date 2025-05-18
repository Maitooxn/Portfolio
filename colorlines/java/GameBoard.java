package colorlines;

import java.util.ArrayList;
import java.util.List;

/**
 * Classe représentant le plateau de jeu ColorLines
 * Gère la grille de jeu et la logique de détection des alignements
 * @author Jordan Oshoffa
 */
public class GameBoard {
    private int size;
    private Ball[][] grid;
    
    /**
     * Constructeur initialisant un plateau vide
     */
    public GameBoard(int size) {
        this.size = size;
        this.grid = new Ball[size][size];
    }
    
    /**
     * Récupère une bille à une position donnée
     */
    public Ball getBall(int x, int y) {
        if (isValidPosition(x, y)) {
            return grid[y][x];
        }
        return null;
    }
    
    /**
     * Place une bille à une position donnée
     */
    public void setBall(int x, int y, Ball ball) {
        if (isValidPosition(x, y)) {
            grid[y][x] = ball;
        }
    }
    
    /**
     * Vérifie si une position est valide
     */
    public boolean isValidPosition(int x, int y) {
        return x >= 0 && x < size && y >= 0 && y < size;
    }
    
    /**
     * Vérifie si une position est vide
     */
    public boolean isEmpty(int x, int y) {
        return isValidPosition(x, y) && grid[y][x] == null;
    }
    
    /**
     * Vérifie si le plateau est plein
     */
    public boolean isFull() {
        for (int y = 0; y < size; y++) {
            for (int x = 0; x < size; x++) {
                if (grid[y][x] == null) {
                    return false;
                }
            }
        }
        return true;
    }
    
    /**
     * Efface le plateau
     */
    public void clear() {
        for (int y = 0; y < size; y++) {
            for (int x = 0; x < size; x++) {
                grid[y][x] = null;
            }
        }
    }
    
    /**
     * Trouve les alignements de billes de longueur minimale spécifiée
     * @param minLength Longueur minimale des alignements à trouver
     * @return Liste des alignements trouvés sous forme de tableaux [x, y, dx, dy, length]
     */
    public List<int[]> findLines(int minLength) {
        List<int[]> lines = new ArrayList<>();
        
        // Vérifier les lignes horizontales
        for (int y = 0; y < size; y++) {
            for (int x = 0; x <= size - minLength; x++) {
                if (grid[y][x] != null) {
                    int length = 1;
                    int colorIndex = grid[y][x].getColorIndex();
                    
                    for (int i = 1; x + i < size; i++) {
                        if (grid[y][x + i] != null && grid[y][x + i].getColorIndex() == colorIndex) {
                            length++;
                        } else {
                            break;
                        }
                    }
                    
                    if (length >= minLength) {
                        lines.add(new int[]{x, y, 1, 0, length});
                        x += length - 1; // Sauter les positions déjà vérifiées
                    }
                }
            }
        }
        
        // Vérifier les lignes verticales
        for (int x = 0; x < size; x++) {
            for (int y = 0; y <= size - minLength; y++) {
                if (grid[y][x] != null) {
                    int length = 1;
                    int colorIndex = grid[y][x].getColorIndex();
                    
                    for (int i = 1; y + i < size; i++) {
                        if (grid[y + i][x] != null && grid[y + i][x].getColorIndex() == colorIndex) {
                            length++;
                        } else {
                            break;
                        }
                    }
                    
                    if (length >= minLength) {
                        lines.add(new int[]{x, y, 0, 1, length});
                        y += length - 1; // Sauter les positions déjà vérifiées
                    }
                }
            }
        }
        
        // Vérifier les diagonales (haut-gauche à bas-droite)
        for (int y = 0; y <= size - minLength; y++) {
            for (int x = 0; x <= size - minLength; x++) {
                if (grid[y][x] != null) {
                    int length = 1;
                    int colorIndex = grid[y][x].getColorIndex();
                    
                    for (int i = 1; x + i < size && y + i < size; i++) {
                        if (grid[y + i][x + i] != null && grid[y + i][x + i].getColorIndex() == colorIndex) {
                            length++;
                        } else {
                            break;
                        }
                    }
                    
                    if (length >= minLength) {
                        lines.add(new int[]{x, y, 1, 1, length});
                    }
                }
            }
        }
        
        // Vérifier les diagonales (haut-droite à bas-gauche)
        for (int y = 0; y <= size - minLength; y++) {
            for (int x = minLength - 1; x < size; x++) {
                if (grid[y][x] != null) {
                    int length = 1;
                    int colorIndex = grid[y][x].getColorIndex();
                    
                    for (int i = 1; x - i >= 0 && y + i < size; i++) {
                        if (grid[y + i][x - i] != null && grid[y + i][x - i].getColorIndex() == colorIndex) {
                            length++;
                        } else {
                            break;
                        }
                    }
                    
                    if (length >= minLength) {
                        lines.add(new int[]{x, y, -1, 1, length});
                    }
                }
            }
        }
        
        return lines;
    }
    
    /**
     * Vérifie s'il y a des alignements de longueur minimale spécifiée
     */
    public boolean hasLines(int minLength) {
        return !findLines(minLength).isEmpty();
    }
    
    /**
     * Retourne la taille du plateau
     */
    public int getSize() {
        return size;
    }
}
