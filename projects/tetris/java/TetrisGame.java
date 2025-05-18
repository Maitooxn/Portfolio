package tetris;

import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.stage.Stage;

/**
 * Classe principale du jeu Tetris en Java
 * Implémente l'interface graphique et la logique du jeu
 * @author Jordan Oshoffa
 */
public class TetrisGame extends Application {
    // Constantes du jeu
    private static final int BLOCK_SIZE = 30;
    private static final int BOARD_WIDTH = 10;
    private static final int BOARD_HEIGHT = 20;
    private static final int CANVAS_WIDTH = BOARD_WIDTH * BLOCK_SIZE;
    private static final int CANVAS_HEIGHT = BOARD_HEIGHT * BLOCK_SIZE;
    private static final int NEXT_PIECE_CANVAS_SIZE = 5 * BLOCK_SIZE;
    
    // Variables du jeu
    private Canvas gameCanvas;
    private Canvas nextPieceCanvas;
    private GraphicsContext gc;
    private GraphicsContext nextPieceGc;
    private GameBoard board;
    private Tetromino currentPiece;
    private Tetromino nextPiece;
    private ScoreManager scoreManager;
    private boolean gameOver = false;
    private boolean paused = false;
    private long lastUpdate = 0;
    private long dropInterval = 1_000_000_000; // 1 seconde en nanosecondes
    
    // Interface utilisateur
    private Text scoreText;
    private Text levelText;
    private Text linesText;
    
    @Override
    public void start(Stage primaryStage) {
        // Initialisation du jeu
        board = new GameBoard(BOARD_WIDTH, BOARD_HEIGHT);
        scoreManager = new ScoreManager();
        
        // Création des pièces initiales
        currentPiece = Tetromino.getRandomPiece();
        nextPiece = Tetromino.getRandomPiece();
        
        // Configuration de l'interface
        BorderPane root = new BorderPane();
        root.setStyle("-fx-background-color: #121212;");
        
        // Canvas principal pour le jeu
        gameCanvas = new Canvas(CANVAS_WIDTH, CANVAS_HEIGHT);
        gc = gameCanvas.getGraphicsContext2D();
        
        // Canvas pour la prochaine pièce
        nextPieceCanvas = new Canvas(NEXT_PIECE_CANVAS_SIZE, NEXT_PIECE_CANVAS_SIZE);
        nextPieceGc = nextPieceCanvas.getGraphicsContext2D();
        
        // Textes d'information
        scoreText = new Text("Score: 0");
        scoreText.setFont(Font.font("Monospace", 20));
        scoreText.setFill(Color.WHITE);
        
        levelText = new Text("Niveau: 1");
        levelText.setFont(Font.font("Monospace", 20));
        levelText.setFill(Color.WHITE);
        
        linesText = new Text("Lignes: 0");
        linesText.setFont(Font.font("Monospace", 20));
        linesText.setFill(Color.WHITE);
        
        // Organisation des éléments d'interface
        VBox infoPanel = new VBox(20);
        infoPanel.setStyle("-fx-padding: 20; -fx-background-color: #1E1E1E;");
        infoPanel.getChildren().addAll(
            new Text("Prochaine pièce:"),
            nextPieceCanvas,
            scoreText,
            levelText,
            linesText
        );
        
        root.setCenter(gameCanvas);
        root.setRight(infoPanel);
        
        // Création de la scène
        Scene scene = new Scene(root);
        
        // Gestion des entrées clavier
        scene.setOnKeyPressed(e -> {
            if (gameOver || paused) return;
            
            switch (e.getCode()) {
                case LEFT:
                    moveLeft();
                    break;
                case RIGHT:
                    moveRight();
                    break;
                case DOWN:
                    moveDown();
                    break;
                case UP:
                    rotate();
                    break;
                case SPACE:
                    hardDrop();
                    break;
                case P:
                    paused = !paused;
                    break;
                default:
                    break;
            }
            
            render();
        });
        
        // Configuration de la fenêtre
        primaryStage.setTitle("Tetris - Jordan Oshoffa");
        primaryStage.setScene(scene);
        primaryStage.setResizable(false);
        primaryStage.show();
        
        // Boucle de jeu
        AnimationTimer gameLoop = new AnimationTimer() {
            @Override
            public void handle(long now) {
                if (paused || gameOver) return;
                
                if (now - lastUpdate >= dropInterval) {
                    update();
                    lastUpdate = now;
                }
            }
        };
        
        gameLoop.start();
        render();
    }
    
    /**
     * Met à jour l'état du jeu
     */
    private void update() {
        if (!moveDown()) {
            // La pièce ne peut plus descendre
            board.placePiece(currentPiece);
            
            // Vérifier les lignes complètes
            int linesCleared = board.clearLines();
            if (linesCleared > 0) {
                scoreManager.addLines(linesCleared);
                updateSpeed();
                updateUI();
            }
            
            // Préparer la prochaine pièce
            currentPiece = nextPiece;
            nextPiece = Tetromino.getRandomPiece();
            
            // Vérifier si le jeu est terminé
            if (!board.isValidPosition(currentPiece)) {
                gameOver = true;
            }
        }
        
        render();
    }
    
    /**
     * Met à jour la vitesse du jeu en fonction du niveau
     */
    private void updateSpeed() {
        // Réduire l'intervalle de chute en fonction du niveau
        dropInterval = Math.max(100_000_000, 1_000_000_000 - (scoreManager.getLevel() - 1) * 50_000_000);
    }
    
    /**
     * Met à jour l'interface utilisateur
     */
    private void updateUI() {
        scoreText.setText("Score: " + scoreManager.getScore());
        levelText.setText("Niveau: " + scoreManager.getLevel());
        linesText.setText("Lignes: " + scoreManager.getLines());
    }
    
    /**
     * Déplace la pièce vers la gauche
     */
    private boolean moveLeft() {
        currentPiece.moveLeft();
        if (!board.isValidPosition(currentPiece)) {
            currentPiece.moveRight(); // Annuler le mouvement
            return false;
        }
        return true;
    }
    
    /**
     * Déplace la pièce vers la droite
     */
    private boolean moveRight() {
        currentPiece.moveRight();
        if (!board.isValidPosition(currentPiece)) {
            currentPiece.moveLeft(); // Annuler le mouvement
            return false;
        }
        return true;
    }
    
    /**
     * Déplace la pièce vers le bas
     */
    private boolean moveDown() {
        currentPiece.moveDown();
        if (!board.isValidPosition(currentPiece)) {
            currentPiece.moveUp(); // Annuler le mouvement
            return false;
        }
        return true;
    }
    
    /**
     * Fait pivoter la pièce
     */
    private void rotate() {
        currentPiece.rotate();
        if (!board.isValidPosition(currentPiece)) {
            currentPiece.rotateBack(); // Annuler la rotation
        }
    }
    
    /**
     * Fait tomber la pièce instantanément
     */
    private void hardDrop() {
        while (moveDown()) {
            // Continuer à descendre jusqu'à ce que ce ne soit plus possible
        }
    }
    
    /**
     * Dessine l'état actuel du jeu
     */
    private void render() {
        // Effacer le canvas
        gc.setFill(Color.BLACK);
        gc.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
        
        // Dessiner la grille
        gc.setStroke(Color.DARKGRAY);
        for (int i = 0; i <= BOARD_WIDTH; i++) {
            gc.strokeLine(i * BLOCK_SIZE, 0, i * BLOCK_SIZE, CANVAS_HEIGHT);
        }
        for (int i = 0; i <= BOARD_HEIGHT; i++) {
            gc.strokeLine(0, i * BLOCK_SIZE, CANVAS_WIDTH, i * BLOCK_SIZE);
        }
        
        // Dessiner les blocs placés
        for (int y = 0; y < BOARD_HEIGHT; y++) {
            for (int x = 0; x < BOARD_WIDTH; x++) {
                if (board.getGrid()[y][x] != 0) {
                    drawBlock(gc, x, y, board.getGrid()[y][x]);
                }
            }
        }
        
        // Dessiner la pièce actuelle
        for (int[] pos : currentPiece.getBlockPositions()) {
            drawBlock(gc, pos[0], pos[1], currentPiece.getColorCode());
        }
        
        // Dessiner la prochaine pièce
        nextPieceGc.setFill(Color.BLACK);
        nextPieceGc.fillRect(0, 0, NEXT_PIECE_CANVAS_SIZE, NEXT_PIECE_CANVAS_SIZE);
        
        int offsetX = 2;
        int offsetY = 2;
        for (int[] pos : nextPiece.getBlockPositions()) {
            int x = pos[0] - nextPiece.getX() + offsetX;
            int y = pos[1] - nextPiece.getY() + offsetY;
            drawBlock(nextPieceGc, x, y, nextPiece.getColorCode());
        }
        
        // Afficher le message de fin de jeu
        if (gameOver) {
            gc.setFill(new Color(0, 0, 0, 0.7));
            gc.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
            
            gc.setFill(Color.WHITE);
            gc.setFont(Font.font("Arial", 30));
            gc.fillText("GAME OVER", CANVAS_WIDTH / 2 - 100, CANVAS_HEIGHT / 2);
            gc.setFont(Font.font("Arial", 20));
            gc.fillText("Score final: " + scoreManager.getScore(), CANVAS_WIDTH / 2 - 80, CANVAS_HEIGHT / 2 + 40);
        }
        
        // Afficher le message de pause
        if (paused) {
            gc.setFill(new Color(0, 0, 0, 0.7));
            gc.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
            
            gc.setFill(Color.WHITE);
            gc.setFont(Font.font("Arial", 30));
            gc.fillText("PAUSE", CANVAS_WIDTH / 2 - 50, CANVAS_HEIGHT / 2);
        }
    }
    
    /**
     * Dessine un bloc à la position spécifiée
     */
    private void drawBlock(GraphicsContext gc, int x, int y, int colorCode) {
        Color color;
        switch (colorCode) {
            case 1: color = Color.CYAN; break;
            case 2: color = Color.BLUE; break;
            case 3: color = Color.ORANGE; break;
            case 4: color = Color.YELLOW; break;
            case 5: color = Color.GREEN; break;
            case 6: color = Color.PURPLE; break;
            case 7: color = Color.RED; break;
            default: color = Color.GRAY;
        }
        
        gc.setFill(color);
        gc.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        
        gc.setStroke(Color.WHITE);
        gc.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        
        // Effet 3D
        gc.setFill(Color.WHITE.deriveColor(0, 1, 1, 0.3));
        gc.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, 5);
        gc.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, 5, BLOCK_SIZE);
        
        gc.setFill(Color.BLACK.deriveColor(0, 1, 1, 0.3));
        gc.fillRect(x * BLOCK_SIZE + BLOCK_SIZE - 5, y * BLOCK_SIZE, 5, BLOCK_SIZE);
        gc.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE + BLOCK_SIZE - 5, BLOCK_SIZE, 5);
    }
    
    /**
     * Point d'entrée du programme
     */
    public static void main(String[] args) {
        launch(args);
    }
}
