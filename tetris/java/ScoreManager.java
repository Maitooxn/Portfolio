package tetris;

/**
 * Classe gérant le score, le niveau et les lignes dans le jeu Tetris
 * @author Jordan Oshoffa
 */
public class ScoreManager {
    private int score;
    private int level;
    private int lines;
    
    // Points par nombre de lignes effacées simultanément
    private static final int[] POINTS_PER_LINES = {0, 40, 100, 300, 1200};
    
    /**
     * Constructeur initialisant les valeurs à zéro
     */
    public ScoreManager() {
        this.score = 0;
        this.level = 1;
        this.lines = 0;
    }
    
    /**
     * Ajoute des points au score en fonction du nombre de lignes effacées
     */
    public void addLines(int linesCleared) {
        if (linesCleared > 0 && linesCleared <= 4) {
            // Calculer les points en fonction du niveau et du nombre de lignes
            int points = POINTS_PER_LINES[linesCleared] * level;
            score += points;
            
            // Mettre à jour le nombre total de lignes
            lines += linesCleared;
            
            // Mettre à jour le niveau (1 niveau tous les 10 lignes)
            level = (lines / 10) + 1;
        }
    }
    
    /**
     * Ajoute des points pour une descente rapide
     */
    public void addSoftDropPoints(int cells) {
        score += cells;
    }
    
    /**
     * Ajoute des points pour une chute instantanée
     */
    public void addHardDropPoints(int cells) {
        score += cells * 2;
    }
    
    /**
     * Réinitialise le score, le niveau et les lignes
     */
    public void reset() {
        score = 0;
        level = 1;
        lines = 0;
    }
    
    // Getters
    
    public int getScore() {
        return score;
    }
    
    public int getLevel() {
        return level;
    }
    
    public int getLines() {
        return lines;
    }
}
