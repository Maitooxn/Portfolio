package colorlines;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

/**
 * Classe gérant le score et les records dans le jeu ColorLines
 * @author Jordan Oshoffa
 */
public class ScoreManager {
    private int score;
    private int highScore;
    private static final String HIGH_SCORE_FILE = "highscore.txt";
    
    /**
     * Constructeur initialisant le score à zéro et chargeant le meilleur score
     */
    public ScoreManager() {
        this.score = 0;
        this.highScore = loadHighScore();
    }
    
    /**
     * Ajoute des points au score
     * @param points Points à ajouter
     */
    public void addScore(int points) {
        // Formule de score : points au carré * 10
        this.score += points * points * 10;
    }
    
    /**
     * Réinitialise le score
     */
    public void resetScore() {
        this.score = 0;
    }
    
    /**
     * Met à jour le meilleur score si nécessaire
     */
    public void updateHighScore() {
        if (score > highScore) {
            highScore = score;
            saveHighScore();
        }
    }
    
    /**
     * Charge le meilleur score depuis un fichier
     */
    private int loadHighScore() {
        try {
            File file = new File(HIGH_SCORE_FILE);
            if (file.exists()) {
                String content = new String(Files.readAllBytes(Paths.get(HIGH_SCORE_FILE)));
                return Integer.parseInt(content.trim());
            }
        } catch (IOException | NumberFormatException e) {
            // En cas d'erreur, retourner 0
        }
        return 0;
    }
    
    /**
     * Sauvegarde le meilleur score dans un fichier
     */
    private void saveHighScore() {
        try (FileWriter writer = new FileWriter(HIGH_SCORE_FILE)) {
            writer.write(String.valueOf(highScore));
        } catch (IOException e) {
            // Ignorer les erreurs d'écriture
        }
    }
    
    /**
     * Retourne le score actuel
     */
    public int getScore() {
        return score;
    }
    
    /**
     * Retourne le meilleur score
     */
    public int getHighScore() {
        return highScore;
    }
}
