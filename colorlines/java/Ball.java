package colorlines;

import javafx.scene.paint.Color;

/**
 * Classe représentant une bille dans le jeu ColorLines
 * @author Jordan Oshoffa
 */
public class Ball {
    private int colorIndex;
    private Color color;
    
    /**
     * Constructeur
     * @param colorIndex Index de la couleur
     * @param color Couleur de la bille
     */
    public Ball(int colorIndex, Color color) {
        this.colorIndex = colorIndex;
        this.color = color;
    }
    
    /**
     * Retourne l'index de la couleur
     */
    public int getColorIndex() {
        return colorIndex;
    }
    
    /**
     * Retourne la couleur de la bille
     */
    public Color getColor() {
        return color;
    }
}
