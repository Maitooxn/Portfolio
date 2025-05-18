package colorlines;

import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Classe principale du jeu ColorLines en Java
 * Implémente l'interface graphique et la logique du jeu
 * @author Jordan Oshoffa
 */
public class ColorLinesGame extends Application {
    // Constantes du jeu
    private static final int CELL_SIZE = 50;
    private static final int BOARD_SIZE = 9;
    private static final int CANVAS_SIZE = BOARD_SIZE * CELL_SIZE;
    private static final int NEW_BALLS_PER_TURN = 3;
    private static final int MIN_LINE_LENGTH = 5;
    
    // Couleurs des billes
    private static final Color[] BALL_COLORS = {
        Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, 
        Color.PURPLE, Color.CYAN, Color.ORANGE
    };
    
    // Variables du jeu
    private Canvas gameCanvas;
    private GraphicsContext gc;
    private GameBoard board;
    private ScoreManager scoreManager;
    private PathFinder pathFinder;
    private Random random;
    
    private int selectedX = -1;
    private int selectedY = -1;
    private boolean animating = false;
    private List<Ball> nextBalls;
    
    // Interface utilisateur
    private Text scoreText;
    private Text highScoreText;
    private Text nextBallsText;
    
    @Override
    public void start(Stage primaryStage) {
        // Initialisation du jeu
        board = new GameBoard(BOARD_SIZE);
        scoreManager = new ScoreManager();
        pathFinder = new PathFinder(board);
        random = new Random();
        nextBalls = new ArrayList<>();
        
        // Configuration de l'interface
        BorderPane root = new BorderPane();
        root.setStyle("-fx-background-color: #121212;");
        
        // Canvas principal pour le jeu
        gameCanvas = new Canvas(CANVAS_SIZE, CANVAS_SIZE);
        gc = gameCanvas.getGraphicsContext2D();
        
        // Textes d'information
        scoreText = new Text("Score: 0");
        scoreText.setFont(Font.font("Monospace", 20));
        scoreText.setFill(Color.WHITE);
        
        highScoreText = new Text("Meilleur score: " + scoreManager.getHighScore());
        highScoreText.setFont(Font.font("Monospace", 20));
        highScoreText.setFill(Color.WHITE);
        
        nextBallsText = new Text("Prochaines billes:");
        nextBallsText.setFont(Font.font("Monospace", 20));
        nextBallsText.setFill(Color.WHITE);
        
        // Organisation des éléments d'interface
        VBox infoPanel = new VBox(20);
        infoPanel.setStyle("-fx-padding: 20; -fx-background-color: #1E1E1E;");
        infoPanel.getChildren().addAll(
            scoreText,
            highScoreText,
            nextBallsText
        );
        
        root.setCenter(gameCanvas);
        root.setRight(infoPanel);
        
        // Gestion des clics souris
        gameCanvas.setOnMouseClicked(this::handleMouseClick);
        
        // Création de la scène
        Scene scene = new Scene(root);
        
        // Configuration de la fenêtre
        primaryStage.setTitle("ColorLines - Jordan Oshoffa");
        primaryStage.setScene(scene);
        primaryStage.setResizable(false);
        primaryStage.show();
        
        // Initialiser le jeu
        startNewGame();
        
        // Boucle de jeu
        AnimationTimer gameLoop = new AnimationTimer() {
            @Override
            public void handle(long now) {
                render();
            }
        };
        
        gameLoop.start();
    }
    
    /**
     * Démarre une nouvelle partie
     */
    private void startNewGame() {
        board.clear();
        scoreManager.resetScore();
        selectedX = -1;
        selectedY = -1;
        animating = false;
        nextBalls = generateNextBalls();
        addNewBalls();
        updateUI();
    }
    
    /**
     * Génère les prochaines billes à apparaître
     */
    private List<Ball> generateNextBalls() {
        List<Ball> balls = new ArrayList<>();
        for (int i = 0; i < NEW_BALLS_PER_TURN; i++) {
            int colorIndex = random.nextInt(BALL_COLORS.length);
            balls.add(new Ball(colorIndex, BALL_COLORS[colorIndex]));
        }
        return balls;
    }
    
    /**
     * Ajoute de nouvelles billes au plateau
     */
    private void addNewBalls() {
        if (board.isFull()) {
            gameOver();
            return;
        }
        
        for (Ball ball : nextBalls) {
            int x, y;
            do {
                x = random.nextInt(BOARD_SIZE);
                y = random.nextInt(BOARD_SIZE);
            } while (board.getBall(x, y) != null);
            
            board.setBall(x, y, ball);
        }
        
        // Vérifier les alignements après avoir ajouté les nouvelles billes
        checkLines();
        
        // Générer les prochaines billes
        nextBalls = generateNextBalls();
        
        // Vérifier si le plateau est plein
        if (board.isFull()) {
            gameOver();
        }
    }
    
    /**
     * Vérifie s'il y a des alignements de billes
     */
    private void checkLines() {
        List<int[]> lines = board.findLines(MIN_LINE_LENGTH);
        if (!lines.isEmpty()) {
            int totalBalls = 0;
            
            for (int[] line : lines) {
                int x = line[0];
                int y = line[1];
                int dx = line[2];
                int dy = line[3];
                int length = line[4];
                
                totalBalls += length;
                
                // Supprimer les billes de la ligne
                for (int i = 0; i < length; i++) {
                    board.setBall(x + i * dx, y + i * dy, null);
                }
            }
            
            // Mettre à jour le score
            scoreManager.addScore(totalBalls);
            updateUI();
        }
    }
    
    /**
     * Gère les clics de souris
     */
    private void handleMouseClick(MouseEvent event) {
        if (animating || board.isFull()) return;
        
        int x = (int) (event.getX() / CELL_SIZE);
        int y = (int) (event.getY() / CELL_SIZE);
        
        if (x < 0 || x >= BOARD_SIZE || y < 0 || y >= BOARD_SIZE) return;
        
        if (selectedX == -1) {
            // Aucune bille sélectionnée, essayer d'en sélectionner une
            if (board.getBall(x, y) != null) {
                selectedX = x;
                selectedY = y;
            }
        } else {
            // Une bille est déjà sélectionnée
            if (x == selectedX && y == selectedY) {
                // Désélectionner la bille
                selectedX = -1;
                selectedY = -1;
            } else if (board.getBall(x, y) == null) {
                // Essayer de déplacer la bille vers une case vide
                List<Point> path = pathFinder.findPath(
                    new Point(selectedX, selectedY), 
                    new Point(x, y)
                );
                
                if (path != null && !path.isEmpty()) {
                    // Déplacer la bille
                    Ball ball = board.getBall(selectedX, selectedY);
                    board.setBall(selectedX, selectedY, null);
                    board.setBall(x, y, ball);
                    
                    // Réinitialiser la sélection
                    selectedX = -1;
                    selectedY = -1;
                    
                    // Vérifier les alignements
                    checkLines();
                    
                    // Ajouter de nouvelles billes si aucun alignement n'a été trouvé
                    if (!board.hasLines(MIN_LINE_LENGTH)) {
                        addNewBalls();
                    }
                }
            } else {
                // Sélectionner une autre bille
                selectedX = x;
                selectedY = y;
            }
        }
    }
    
    /**
     * Fin de partie
     */
    private void gameOver() {
        // Sauvegarder le meilleur score
        scoreManager.updateHighScore();
        updateUI();
    }
    
    /**
     * Met à jour l'interface utilisateur
     */
    private void updateUI() {
        scoreText.setText("Score: " + scoreManager.getScore());
        highScoreText.setText("Meilleur score: " + scoreManager.getHighScore());
    }
    
    /**
     * Dessine l'état actuel du jeu
     */
    private void render() {
        // Effacer le canvas
        gc.setFill(Color.BLACK);
        gc.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
        
        // Dessiner la grille
        gc.setStroke(Color.DARKGRAY);
        for (int i = 0; i <= BOARD_SIZE; i++) {
            gc.strokeLine(i * CELL_SIZE, 0, i * CELL_SIZE, CANVAS_SIZE);
            gc.strokeLine(0, i * CELL_SIZE, CANVAS_SIZE, i * CELL_SIZE);
        }
        
        // Dessiner les billes
        for (int y = 0; y < BOARD_SIZE; y++) {
            for (int x = 0; x < BOARD_SIZE; x++) {
                Ball ball = board.getBall(x, y);
                if (ball != null) {
                    drawBall(x, y, ball.getColor(), x == selectedX && y == selectedY);
                }
            }
        }
        
        // Dessiner les prochaines billes
        for (int i = 0; i < nextBalls.size(); i++) {
            Ball ball = nextBalls.get(i);
            gc.setFill(ball.getColor());
            gc.fillOval(CANVAS_SIZE - 30, 100 + i * 60, 20, 20);
        }
        
        // Afficher le message de fin de jeu
        if (board.isFull()) {
            gc.setFill(new Color(0, 0, 0, 0.7));
            gc.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
            
            gc.setFill(Color.WHITE);
            gc.setFont(Font.font("Arial", 30));
            gc.fillText("GAME OVER", CANVAS_SIZE / 2 - 100, CANVAS_SIZE / 2);
            gc.setFont(Font.font("Arial", 20));
            gc.fillText("Score final: " + scoreManager.getScore(), CANVAS_SIZE / 2 - 80, CANVAS_SIZE / 2 + 40);
            gc.fillText("Appuyez sur R pour recommencer", CANVAS_SIZE / 2 - 150, CANVAS_SIZE / 2 + 80);
        }
    }
    
    /**
     * Dessine une bille à la position spécifiée
     */
    private void drawBall(int x, int y, Color color, boolean selected) {
        double centerX = x * CELL_SIZE + CELL_SIZE / 2;
        double centerY = y * CELL_SIZE + CELL_SIZE / 2;
        double radius = CELL_SIZE / 2 - 5;
        
        if (selected) {
            // Dessiner un halo autour de la bille sélectionnée
            gc.setFill(Color.WHITE.deriveColor(0, 1, 1, 0.3));
            gc.fillOval(centerX - radius - 3, centerY - radius - 3, 
                       (radius + 3) * 2, (radius + 3) * 2);
        }
        
        // Dessiner la bille
        gc.setFill(color);
        gc.fillOval(centerX - radius, centerY - radius, radius * 2, radius * 2);
        
        // Effet 3D
        gc.setFill(Color.WHITE.deriveColor(0, 1, 1, 0.7));
        gc.fillOval(centerX - radius / 2, centerY - radius / 2, radius / 2, radius / 2);
    }
    
    /**
     * Point d'entrée du programme
     */
    public static void main(String[] args) {
        launch(args);
    }
}
