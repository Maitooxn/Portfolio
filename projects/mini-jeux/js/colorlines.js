/**
 * Color Lines - Jeu de réflexion où le joueur doit aligner des billes de même couleur
 * Conversion JavaScript du jeu Python original
 */

class ColorLines {
    constructor(canvasId, nextBallsCanvasId, scoreCanvasId) {
        // Initialisation des structures de données
        this.gridSize = 9;       // nombre de lignes et de colonnes du plateau
        this.boardSize = 450;    // taille du plateau en pixels
        this.cellSize = this.boardSize / this.gridSize;
        this.grid = [];
        this.validDestinations = new Set();
        this.initialBalls = 3;
        this.nextBallsCount = 3;
        this.selectedCell = null;
        this.colors = ["red", "blue", "green", "yellow", "magenta", "orange", "cyan"];
        this.nextBalls = [];
        this.score = 0;
        
        // Initialisation des éléments graphiques
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.canvas.width = this.boardSize;
        this.canvas.height = this.boardSize;
        
        this.nextBallsCanvas = document.getElementById(nextBallsCanvasId);
        this.nextBallsCtx = this.nextBallsCanvas.getContext('2d');
        this.nextBallsCanvas.width = this.cellSize * 4;
        this.nextBallsCanvas.height = this.cellSize;
        
        this.scoreCanvas = document.getElementById(scoreCanvasId);
        this.scoreCtx = this.scoreCanvas.getContext('2d');
        this.scoreCanvas.width = this.cellSize * 3;
        this.scoreCanvas.height = this.cellSize;
        
        // Ajout des écouteurs d'événements
        this.canvas.addEventListener('click', this.handleClick.bind(this));
        
        // Initialisation du jeu
        this.initGame();
    }
    
    initGame() {
        // Réinitialisation du jeu
        this.validDestinations = new Set();
        this.score = 0;
        this.nextBalls = this.generateNextBalls(this.nextBallsCount);
        this.initGrid();
        this.refreshNextBalls();
        this.refreshScore();
    }
    
    initGrid() {
        // Initialise la grille avec quelques boules placées aléatoirement
        this.grid = Array(this.gridSize).fill().map(() => Array(this.gridSize).fill(null));
        
        // Création d'une liste de toutes les positions possibles
        let positions = [];
        for (let i = 0; i < this.gridSize; i++) {
            for (let j = 0; j < this.gridSize; j++) {
                positions.push([i, j]);
            }
        }
        
        // Mélange des positions
        this.shuffleArray(positions);
        
        // Placement des boules initiales
        for (let i = 0; i < this.initialBalls; i++) {
            if (positions.length === 0) break;
            let [row, col] = positions.pop();
            this.grid[row][col] = this.colors[Math.floor(Math.random() * this.colors.length)];
        }
        
        this.refreshBoard();
    }
    
    generateNextBalls(count) {
        // Génère les prochaines boules à placer
        let balls = [];
        for (let i = 0; i < count; i++) {
            balls.push(this.colors[Math.floor(Math.random() * this.colors.length)]);
        }
        return balls;
    }
    
    refreshBoard() {
        // Redessine le plateau de jeu
        this.ctx.clearRect(0, 0, this.boardSize, this.boardSize);
        
        // Dessiner les cases
        for (let i = 0; i < this.gridSize; i++) {
            for (let j = 0; j < this.gridSize; j++) {
                // Couleur de fond de la case
                let cellColor = "lightgray";
                if (this.validDestinations.has(`${i},${j}`)) {
                    cellColor = "lightgreen";
                }
                
                // Dessiner la case
                this.ctx.fillStyle = cellColor;
                this.ctx.fillRect(j * this.cellSize, i * this.cellSize, this.cellSize, this.cellSize);
                this.ctx.strokeStyle = "black";
                this.ctx.strokeRect(j * this.cellSize, i * this.cellSize, this.cellSize, this.cellSize);
                
                // Dessiner la boule si présente
                if (this.grid[i][j] !== null) {
                    this.drawBall(j, i, this.grid[i][j]);
                }
            }
        }
        
        // Bordure du plateau
        this.ctx.lineWidth = 3;
        this.ctx.strokeRect(0, 0, this.boardSize, this.boardSize);
        this.ctx.lineWidth = 1;
    }
    
    drawBall(x, y, color) {
        // Dessine une boule à la position (x, y) avec la couleur spécifiée
        const border = 3;
        const centerX = x * this.cellSize + this.cellSize / 2;
        const centerY = y * this.cellSize + this.cellSize / 2;
        const radius = this.cellSize / 2 - border;
        
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
        this.ctx.fillStyle = color;
        this.ctx.fill();
        this.ctx.strokeStyle = "black";
        this.ctx.stroke();
    }
    
    refreshNextBalls() {
        // Affiche les prochaines boules
        this.nextBallsCtx.clearRect(0, 0, this.nextBallsCanvas.width, this.nextBallsCanvas.height);
        
        // Texte "Suivantes:"
        this.nextBallsCtx.fillStyle = "black";
        this.nextBallsCtx.font = "14px Arial";
        this.nextBallsCtx.fillText("Suivantes:", 10, 20);
        
        // Dessiner les boules
        const border = 5;
        for (let i = 0; i < this.nextBalls.length; i++) {
            const centerX = (i + 1.5) * this.cellSize;
            const centerY = this.cellSize / 2;
            const radius = this.cellSize / 3;
            
            this.nextBallsCtx.beginPath();
            this.nextBallsCtx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
            this.nextBallsCtx.fillStyle = this.nextBalls[i];
            this.nextBallsCtx.fill();
            this.nextBallsCtx.strokeStyle = "black";
            this.nextBallsCtx.stroke();
        }
    }
    
    refreshScore() {
        // Affiche le score
        this.scoreCtx.clearRect(0, 0, this.scoreCanvas.width, this.scoreCanvas.height);
        
        // Texte "Score:"
        this.scoreCtx.fillStyle = "black";
        this.scoreCtx.font = "14px Arial";
        this.scoreCtx.fillText("Score:", 10, 20);
        
        // Valeur du score
        this.scoreCtx.font = "16px Arial";
        this.scoreCtx.fillText(this.score.toString(), this.scoreCanvas.width - 50, this.cellSize / 2 + 5);
    }
    
    handleClick(event) {
        // Gère les clics sur le plateau
        const rect = this.canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        const col = Math.floor(x / this.cellSize);
        const row = Math.floor(y / this.cellSize);
        
        if (row >= 0 && row < this.gridSize && col >= 0 && col < this.gridSize) {
            if (this.grid[row][col] !== null) {
                // Clic sur une boule
                if (this.validDestinations.size > 0) {
                    this.validDestinations.clear();
                } else {
                    this.validDestinations = this.getAccessibleCells(row, col);
                    this.selectedCell = [row, col];
                }
                this.refreshBoard();
            } else {
                // Clic sur une case vide
                if (this.selectedCell) {
                    if (this.validDestinations.has(`${row},${col}`)) {
                        this.moveBall(this.selectedCell[0], this.selectedCell[1], row, col);
                        if (!this.removeSeries()) {
                            // Ajouter les nouvelles boules
                            let emptyCells = [];
                            for (let i = 0; i < this.gridSize; i++) {
                                for (let j = 0; j < this.gridSize; j++) {
                                    if (this.grid[i][j] === null) {
                                        emptyCells.push([i, j]);
                                    }
                                }
                            }
                            
                            this.shuffleArray(emptyCells);
                            
                            for (let i = 0; i < this.nextBalls.length; i++) {
                                if (emptyCells.length === 0) break;
                                let [r, c] = emptyCells.pop();
                                this.grid[r][c] = this.nextBalls[i];
                            }
                            
                            this.nextBalls = this.generateNextBalls(this.nextBallsCount);
                            this.refreshGame();
                            this.removeSeries();
                        }
                    } else {
                        this.validDestinations.clear();
                    }
                    this.refreshGame();
                    this.selectedCell = null;
                }
            }
        }
    }
    
    getAccessibleCells(row, col) {
        // Trouve toutes les cases accessibles à partir de la case (row, col)
        let visited = new Set();
        let accessible = new Set();
        
        const explore = (r, c) => {
            const key = `${r},${c}`;
            if (visited.has(key)) return;
            
            visited.add(key);
            
            // Directions: haut, bas, gauche, droite
            const directions = [[-1, 0], [1, 0], [0, -1], [0, 1]];
            
            for (let [dr, dc] of directions) {
                const nr = r + dr;
                const nc = c + dc;
                
                if (nr >= 0 && nr < this.gridSize && nc >= 0 && nc < this.gridSize) {
                    if (this.grid[nr][nc] === null) {
                        accessible.add(`${nr},${nc}`);
                        explore(nr, nc);
                    }
                }
            }
        };
        
        explore(row, col);
        return accessible;
    }
    
    moveBall(fromRow, fromCol, toRow, toCol) {
        // Déplace une boule d'une case à une autre
        if (this.validDestinations.has(`${toRow},${toCol}`)) {
            this.grid[toRow][toCol] = this.grid[fromRow][fromCol];
            this.grid[fromRow][fromCol] = null;
            this.validDestinations.clear();
        }
    }
    
    removeSeries() {
        // Retire les séries de 5 boules ou plus de même couleur
        let cellsToRemove = new Set();
        
        // Vérification horizontale
        for (let i = 0; i < this.gridSize; i++) {
            let count = 1;
            for (let j = 1; j < this.gridSize; j++) {
                if (this.grid[i][j] !== null && this.grid[i][j] === this.grid[i][j-1]) {
                    count++;
                } else {
                    if (count >= 5) {
                        for (let k = j - count; k < j; k++) {
                            cellsToRemove.add(`${i},${k}`);
                        }
                    }
                    count = 1;
                }
            }
            if (count >= 5) {
                for (let k = this.gridSize - count; k < this.gridSize; k++) {
                    cellsToRemove.add(`${i},${k}`);
                }
            }
        }
        
        // Vérification verticale
        for (let j = 0; j < this.gridSize; j++) {
            let count = 1;
            for (let i = 1; i < this.gridSize; i++) {
                if (this.grid[i][j] !== null && this.grid[i][j] === this.grid[i-1][j]) {
                    count++;
                } else {
                    if (count >= 5) {
                        for (let k = i - count; k < i; k++) {
                            cellsToRemove.add(`${k},${j}`);
                        }
                    }
                    count = 1;
                }
            }
            if (count >= 5) {
                for (let k = this.gridSize - count; k < this.gridSize; k++) {
                    cellsToRemove.add(`${k},${j}`);
                }
            }
        }
        
        // Vérification diagonale (haut-gauche à bas-droite)
        for (let k = -this.gridSize + 1; k < this.gridSize; k++) {
            let diag = [];
            for (let i = Math.max(0, -k); i < Math.min(this.gridSize, this.gridSize - k); i++) {
                diag.push([i, i + k]);
            }
            
            let count = 1;
            for (let idx = 1; idx < diag.length; idx++) {
                let [r1, c1] = diag[idx - 1];
                let [r2, c2] = diag[idx];
                
                if (this.grid[r1][c1] !== null && this.grid[r1][c1] === this.grid[r2][c2]) {
                    count++;
                } else {
                    if (count >= 5) {
                        for (let i = idx - count; i < idx; i++) {
                            let [r, c] = diag[i];
                            cellsToRemove.add(`${r},${c}`);
                        }
                    }
                    count = 1;
                }
            }
            
            if (count >= 5) {
                for (let i = diag.length - count; i < diag.length; i++) {
                    let [r, c] = diag[i];
                    cellsToRemove.add(`${r},${c}`);
                }
            }
        }
        
        // Vérification diagonale (haut-droite à bas-gauche)
        for (let k = 0; k < 2 * this.gridSize - 1; k++) {
            let diag = [];
            for (let i = Math.max(0, k - this.gridSize + 1); i < Math.min(this.gridSize, k + 1); i++) {
                diag.push([i, k - i]);
            }
            
            let count = 1;
            for (let idx = 1; idx < diag.length; idx++) {
                let [r1, c1] = diag[idx - 1];
                let [r2, c2] = diag[idx];
                
                if (this.grid[r1][c1] !== null && this.grid[r1][c1] === this.grid[r2][c2]) {
                    count++;
                } else {
                    if (count >= 5) {
                        for (let i = idx - count; i < idx; i++) {
                            let [r, c] = diag[i];
                            cellsToRemove.add(`${r},${c}`);
                        }
                    }
                    count = 1;
                }
            }
            
            if (count >= 5) {
                for (let i = diag.length - count; i < diag.length; i++) {
                    let [r, c] = diag[i];
                    cellsToRemove.add(`${r},${c}`);
                }
            }
        }
        
        // Supprimer les boules et mettre à jour le score
        if (cellsToRemove.size > 0) {
            this.score += 2 * cellsToRemove.size;
            
            for (let cell of cellsToRemove) {
                let [r, c] = cell.split(',').map(Number);
                this.grid[r][c] = null;
            }
            
            return true;
        }
        
        return false;
    }
    
    refreshGame() {
        // Rafraîchit tous les éléments du jeu
        this.refreshBoard();
        this.refreshNextBalls();
        this.refreshScore();
    }
    
    shuffleArray(array) {
        // Mélange un tableau
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
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
    const game = new ColorLines('game-canvas', 'next-balls-canvas', 'score-canvas');
    
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            game.reset();
        });
    }
});
