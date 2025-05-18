package tetris;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Classe représentant une pièce de Tetris (tétromino)
 * Gère la forme, la position et la rotation des pièces
 * @author Jordan Oshoffa
 */
public class Tetromino {
    // Types de pièces (I, J, L, O, S, T, Z)
    private static final int[][][] TETROMINO_SHAPES = {
        // I
        {
            {0, 0, 0, 0},
            {1, 1, 1, 1},
            {0, 0, 0, 0},
            {0, 0, 0, 0}
        },
        // J
        {
            {2, 0, 0},
            {2, 2, 2},
            {0, 0, 0}
        },
        // L
        {
            {0, 0, 3},
            {3, 3, 3},
            {0, 0, 0}
        },
        // O
        {
            {4, 4},
            {4, 4}
        },
        // S
        {
            {0, 5, 5},
            {5, 5, 0},
            {0, 0, 0}
        },
        // T
        {
            {0, 6, 0},
            {6, 6, 6},
            {0, 0, 0}
        },
        // Z
        {
            {7, 7, 0},
            {0, 7, 7},
            {0, 0, 0}
        }
    };
    
    private int[][] shape;
    private int x;
    private int y;
    private int colorCode;
    private static final Random random = new Random();
    
    /**
     * Constructeur pour une pièce spécifique
     */
    public Tetromino(int[][] shape, int colorCode) {
        this.shape = shape;
        this.colorCode = colorCode;
        this.x = 3; // Position initiale au centre
        this.y = 0; // Position initiale en haut
    }
    
    /**
     * Crée une pièce aléatoire
     */
    public static Tetromino getRandomPiece() {
        int index = random.nextInt(TETROMINO_SHAPES.length);
        int[][] shape = TETROMINO_SHAPES[index];
        int colorCode = index + 1; // Code couleur basé sur l'index (1-7)
        return new Tetromino(deepCopy(shape), colorCode);
    }
    
    /**
     * Effectue une copie profonde d'un tableau 2D
     */
    private static int[][] deepCopy(int[][] original) {
        int[][] copy = new int[original.length][];
        for (int i = 0; i < original.length; i++) {
            copy[i] = original[i].clone();
        }
        return copy;
    }
    
    /**
     * Retourne les positions des blocs de la pièce
     */
    public List<int[]> getBlockPositions() {
        List<int[]> positions = new ArrayList<>();
        
        for (int row = 0; row < shape.length; row++) {
            for (int col = 0; col < shape[row].length; col++) {
                if (shape[row][col] != 0) {
                    positions.add(new int[]{x + col, y + row});
                }
            }
        }
        
        return positions;
    }
    
    /**
     * Fait pivoter la pièce dans le sens horaire
     */
    public void rotate() {
        int[][] rotated = new int[shape[0].length][shape.length];
        
        for (int row = 0; row < shape.length; row++) {
            for (int col = 0; col < shape[row].length; col++) {
                rotated[col][shape.length - 1 - row] = shape[row][col];
            }
        }
        
        shape = rotated;
    }
    
    /**
     * Fait pivoter la pièce dans le sens anti-horaire (pour annuler une rotation)
     */
    public void rotateBack() {
        int[][] rotated = new int[shape[0].length][shape.length];
        
        for (int row = 0; row < shape.length; row++) {
            for (int col = 0; col < shape[row].length; col++) {
                rotated[shape[row].length - 1 - col][row] = shape[row][col];
            }
        }
        
        shape = rotated;
    }
    
    /**
     * Déplace la pièce vers la gauche
     */
    public void moveLeft() {
        x--;
    }
    
    /**
     * Déplace la pièce vers la droite
     */
    public void moveRight() {
        x++;
    }
    
    /**
     * Déplace la pièce vers le bas
     */
    public void moveDown() {
        y++;
    }
    
    /**
     * Déplace la pièce vers le haut (pour annuler un mouvement vers le bas)
     */
    public void moveUp() {
        y--;
    }
    
    // Getters et setters
    
    public int getX() {
        return x;
    }
    
    public int getY() {
        return y;
    }
    
    public int[][] getShape() {
        return shape;
    }
    
    public int getColorCode() {
        return colorCode;
    }
    
    public int getWidth() {
        return shape[0].length;
    }
    
    public int getHeight() {
        return shape.length;
    }
}
