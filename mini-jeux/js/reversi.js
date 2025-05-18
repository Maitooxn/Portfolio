/**
 * Reversi - Jeu de stratégie classique aussi connu sous le nom d'Othello
 * Conversion JavaScript du jeu Python original
 */

class Reversi {
    constructor(canvasId, scoreCanvasId1, scoreCanvasId2) {
        // Initialisation des structures de données
        this.gridSize = 8;       // nombre de lignes et de colonnes du plateau
        this.boardSize = 512;    // taille du plateau en pixels
        this.cellSize = this.boardSize / this.gridSize;
        this.grid = [];
        this.currentPlayer = 0;  // 0 = noir (commence), 1 = blanc
        this.colors = ["black", "red"];
        
        // Initialisation des éléments graphiques
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.canvas.width = this.boardSize;
        this.canvas.height = this.boardSize;
        
        this.scoreCanvas1 = document.getElementById(scoreCanvasId1);
        this.scoreCtx1 = this.scoreCanvas1.getContext('2d');
        this.scoreCanvas1.width = this.cellSize;
        this.scoreCanvas1.height = this.cellSize;
        
        this.scoreCanvas2 = document.getElementById(scoreCanvasId2);
        this.scoreCtx2 = this.scoreCanvas2.getContext('2d');
        this.scoreCanvas2.width = this.cellSize;
        this.scoreCanvas2.height = this.cellSize;
        
        // Ajout des écouteurs d'événements
        this.canvas.addEventListener('click', this.handleClick.bind(this));
        
        // Initialisation du jeu
        this.initGame();
    }
    
    initGame() {
        // Réinitialisation du jeu
        this.currentPlayer = 0;  // Noir commence
        this.initGrid();
        this.refreshScores();
        this.updateTitle();
    }
    
    initGrid() {
        // Initialise la grille avec la configuration initiale du jeu
        this.grid = Array(this.gridSize).fill().map(() => Array(this.gridSize).fill(null));
        
        // Configuration initiale : 4 pions au centre
        const middle = this.gridSize / 2;
        this.grid[middle - 1][middle - 1] = 0;  // Noir
        this.grid[middle][middle] = 0;          // Noir
        this.grid[middle - 1][middle] = 1;      // Rouge
        this.grid[middle][middle - 1] = 1;      // Rouge
        
        this.drawBoard();
        this.refreshBoard();
    }
    
    drawBoard() {
        // Dessine la grille du plateau
        this.ctx.clearRect(0, 0, this.boardSize, this.boardSize);
        
        // Fond vert
        this.ctx.fillStyle = "#008000";
        this.ctx.fillRect(0, 0, this.boardSize, this.boardSize);
        
        // Lignes de la grille
        this.ctx.strokeStyle = "black";
        this.ctx.lineWidth = 1;
        
        for (let i = 0; i <= this.gridSize; i++) {
            // Lignes horizontales
            this.ctx.beginPath();
            this.ctx.moveTo(0, i * this.cellSize);
            this.ctx.lineTo(this.boardSize, i * this.cellSize);
            this.ctx.stroke();
            
            // Lignes verticales
            this.ctx.beginPath();
            this.ctx.moveTo(i * this.cellSize, 0);
            this.ctx.lineTo(i * this.cellSize, this.boardSize);
            this.ctx.stroke();
        }
    }
    
    refreshBoard() {
        // Redessine les pions sur le plateau
        const border = 3;
        
        for (let i = 0; i < this.gridSize; i++) {
            for (let j = 0; j < this.gridSize; j++) {
                const cell = this.grid[i][j];
                if (cell !== null) {
                    // Dessiner le pion
                    const centerX = j * this.cellSize + this.cellSize / 2;
                    const centerY = i * this.cellSize + this.cellSize / 2;
                    const radius = this.cellSize / 2 - border;
                    
                    this.ctx.beginPath();
                    this.ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
                    this.ctx.fillStyle = this.colors[cell];
                    this.ctx.fill();
                    this.ctx.strokeStyle = this.colors[cell];
                    this.ctx.stroke();
                }
            }
        }
    }
    
    refreshScores() {
        // Rafraîchit l'affichage des scores
        const border = 3;
        const scores = [this.getScore(0), this.getScore(1)];
        
        // Score joueur 1 (noir)
        this.scoreCtx1.clearRect(0, 0, this.cellSize, this.cellSize);
        this.scoreCtx1.beginPath();
        this.scoreCtx1.arc(this.cellSize / 2, this.cellSize / 2, this.cellSize / 2 - border, 0, 2 * Math.PI);
        this.scoreCtx1.fillStyle = this.colors[0];
        this.scoreCtx1.fill();
        this.scoreCtx1.strokeStyle = this.colors[0];
        this.scoreCtx1.stroke();
        
        this.scoreCtx1.fillStyle = "white";
        this.scoreCtx1.font = "bold 16px Courier";
        this.scoreCtx1.textAlign = "center";
        this.scoreCtx1.textBaseline = "middle";
        this.scoreCtx1.fillText(scores[0].toString(), this.cellSize / 2, this.cellSize / 2);
        
        // Score joueur 2 (rouge)
        this.scoreCtx2.clearRect(0, 0, this.cellSize, this.cellSize);
        this.scoreCtx2.beginPath();
        this.scoreCtx2.arc(this.cellSize / 2, this.cellSize / 2, this.cellSize / 2 - border, 0, 2 * Math.PI);
        this.scoreCtx2.fillStyle = this.colors[1];
        this.scoreCtx2.fill();
        this.scoreCtx2.strokeStyle = this.colors[1];
        this.scoreCtx2.stroke();
        
        this.scoreCtx2.fillStyle = "white";
        this.scoreCtx2.font = "bold 16px Courier";
        this.scoreCtx2.textAlign = "center";
        this.scoreCtx2.textBaseline = "middle";
        this.scoreCtx2.fillText(scores[1].toString(), this.cellSize / 2, this.cellSize / 2);
    }
    
    getScore(player) {
        // Renvoie le score du joueur (nombre de pions)
        let count = 0;
        for (let i = 0; i < this.gridSize; i++) {
            for (let j = 0; j < this.gridSize; j++) {
                if (this.grid[i][j] === player) {
                    count++;
                }
            }
        }
        return count;
    }
    
    updateTitle() {
        // Met à jour le titre avec le joueur actuel
        const titleElement = document.getElementById('game-status');
        if (titleElement) {
            titleElement.textContent = `Tour du joueur ${this.currentPlayer + 1} (${this.colors[this.currentPlayer]})`;
        }
    }
    
    handleClick(event) {
        // Gère les clics sur le plateau
        const rect = this.canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        const col = Math.floor(x / this.cellSize);
        const row = Math.floor(y / this.cellSize);
        
        if (row >= 0 && row < this.gridSize && col >= 0 && col < this.gridSize) {
            if (this.isCellPlayable(row, col)) {
                this.grid[row][col] = this.currentPlayer;  // Placer le pion
                this.applyFlips(row, col);                 // Retourner les pions
                this.currentPlayer = 1 - this.currentPlayer;  // Changer de joueur
                this.refreshBoard();                       // Rafraîchir l'affichage
                this.refreshScores();                      // Mettre à jour les scores
                this.updateTitle();                        // Mettre à jour le titre
            }
        }
    }
    
    isCellPlayable(row, col) {
        // Vérifie si la case est jouable
        if (this.grid[row][col] !== null) {
            return false;
        }
        
        // Vérifier s'il y a au moins un pion adjacent
        for (let dr = -1; dr <= 1; dr++) {
            for (let dc = -1; dc <= 1; dc++) {
                if (dr === 0 && dc === 0) continue;
                
                const nr = row + dr;
                const nc = col + dc;
                
                if (nr >= 0 && nr < this.gridSize && nc >= 0 && nc < this.gridSize && 
                    this.grid[nr][nc] !== null) {
                    // Vérifier si ce mouvement capture des pions
                    if (this.wouldFlip(row, col).length > 0) {
                        return true;
                    }
                }
            }
        }
        
        return false;
    }
    
    wouldFlip(row, col) {
        // Renvoie les coordonnées des pions qui seraient retournés
        const toFlip = [];
        const opponent = 1 - this.currentPlayer;
        
        // Directions: horizontales, verticales et diagonales
        const directions = [
            [-1, 0], [1, 0], [0, -1], [0, 1],  // Verticales et horizontales
            [-1, -1], [-1, 1], [1, -1], [1, 1]  // Diagonales
        ];
        
        for (let [dr, dc] of directions) {
            let r = row + dr;
            let c = col + dc;
            const captured = [];
            
            // Avancer dans la direction tant qu'on trouve des pions adverses
            while (r >= 0 && r < this.gridSize && c >= 0 && c < this.gridSize && 
                   this.grid[r][c] === opponent) {
                captured.push([r, c]);
                r += dr;
                c += dc;
            }
            
            // Si on trouve un de nos pions à la fin, on capture la ligne
            if (r >= 0 && r < this.gridSize && c >= 0 && c < this.gridSize && 
                this.grid[r][c] === this.currentPlayer && captured.length > 0) {
                toFlip.push(...captured);
            }
        }
        
        return toFlip;
    }
    
    applyFlips(row, col) {
        // Applique les retournements de pions après un coup
        const toFlip = this.wouldFlip(row, col);
        
        for (let [r, c] of toFlip) {
            this.grid[r][c] = this.currentPlayer;
        }
    }
    
    reset() {
        // Réinitialise le jeu
        this.initGame();
    }
}

// Initialisation du jeu lorsque la page est chargée
document.addEventListener('DOMContentLoaded', function() {
    const resetButton = document.getElementById('reset-button');
    const game = new Reversi('game-canvas', 'score-canvas-1', 'score-canvas-2');
    
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            game.reset();
        });
    }
});
