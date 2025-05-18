/**
 * Klickety - Jeu de puzzle où vous éliminez des groupes de blocs de même couleur
 * Conversion JavaScript du jeu Python original
 */

class Klickety {
    constructor(canvasId, blocCountCanvasId) {
        // Initialisation des structures de données
        this.gridRows = 16;      // nombre de lignes du plateau
        this.gridCols = 10;      // nombre de colonnes du plateau
        this.cellSize = 32;      // taille d'une case en pixels
        this.boardHeight = this.cellSize * this.gridRows;
        this.boardWidth = this.cellSize * this.gridCols;
        this.grid = [];
        this.colors = ["red", "blue", "green", "yellow", "magenta"];
        this.blocCount = 0;
        
        // Initialisation des éléments graphiques
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.canvas.width = this.boardWidth;
        this.canvas.height = this.boardHeight;
        
        this.blocCountCanvas = document.getElementById(blocCountCanvasId);
        this.blocCountCtx = this.blocCountCanvas.getContext('2d');
        this.blocCountCanvas.width = this.boardWidth;
        this.blocCountCanvas.height = 32;
        
        // Ajout des écouteurs d'événements
        this.canvas.addEventListener('click', this.handleClick.bind(this));
        
        // Initialisation du jeu
        this.initGame();
    }
    
    initGame() {
        // Réinitialisation du jeu
        this.initGrid();
        this.refreshBlocCount();
    }
    
    initGrid() {
        // Initialise la grille avec des blocs de couleurs aléatoires
        this.grid = [];
        for (let i = 0; i < this.gridRows; i++) {
            let row = [];
            for (let j = 0; j < this.gridCols; j++) {
                row.push(this.colors[Math.floor(Math.random() * this.colors.length)]);
            }
            this.grid.push(row);
        }
        
        this.refreshBoard();
    }
    
    refreshBoard() {
        // Redessine le plateau de jeu
        this.ctx.clearRect(0, 0, this.boardWidth, this.boardHeight);
        
        // Dessiner les blocs
        const backgroundColor = "black";
        
        for (let i = 0; i < this.gridRows; i++) {
            for (let j = 0; j < this.gridCols; j++) {
                const cell = this.grid[i][j];
                
                if (cell !== null) {
                    // Dessiner un bloc coloré
                    this.ctx.fillStyle = cell;
                    this.ctx.fillRect(j * this.cellSize, i * this.cellSize, this.cellSize, this.cellSize);
                    this.ctx.strokeStyle = cell;
                    this.ctx.strokeRect(j * this.cellSize, i * this.cellSize, this.cellSize, this.cellSize);
                } else {
                    // Dessiner un espace vide
                    this.ctx.fillStyle = backgroundColor;
                    this.ctx.fillRect(j * this.cellSize, i * this.cellSize, this.cellSize, this.cellSize);
                    this.ctx.strokeStyle = backgroundColor;
                    this.ctx.strokeRect(j * this.cellSize, i * this.cellSize, this.cellSize, this.cellSize);
                }
            }
        }
        
        // Tracer le contour des pièces
        // 1) Séparations entre deux pièces adjacentes de couleurs différentes dans la même colonne
        for (let j = 0; j < this.gridCols; j++) {
            for (let i = 1; i < this.gridRows; i++) {
                if (this.grid[i-1][j] !== this.grid[i][j] && 
                    this.grid[i-1][j] !== null && this.grid[i][j] !== null) {
                    this.ctx.fillStyle = backgroundColor;
                    this.ctx.fillRect(j * this.cellSize, i * this.cellSize, this.cellSize, 1);
                }
            }
        }
        
        // 2) Séparations entre deux pièces adjacentes de couleurs différentes dans la même ligne
        for (let i = 0; i < this.gridRows; i++) {
            for (let j = 1; j < this.gridCols; j++) {
                if (this.grid[i][j-1] !== this.grid[i][j] && 
                    this.grid[i][j-1] !== null && this.grid[i][j] !== null) {
                    this.ctx.fillStyle = backgroundColor;
                    this.ctx.fillRect(j * this.cellSize, i * this.cellSize, 1, this.cellSize);
                }
            }
        }
    }
    
    refreshBlocCount(piece = null) {
        // Rafraîchit l'affichage du nombre de blocs restants
        this.blocCountCtx.clearRect(0, 0, this.blocCountCanvas.width, this.blocCountCanvas.height);
        
        if (piece === null) {
            // Appel initial, tous les blocs sont encore présents
            this.blocCount = this.gridRows * this.gridCols;
        } else {
            // Soustraire du nombre de blocs celui de la pièce retirée
            this.blocCount -= piece.size;
        }
        
        this.blocCountCtx.fillStyle = "black";
        this.blocCountCtx.font = "14px Arial";
        this.blocCountCtx.textAlign = "center";
        this.blocCountCtx.fillText("Blocs restants: " + this.blocCount, this.boardWidth / 2, this.cellSize / 2 + 5);
    }
    
    handleClick(event) {
        // Gère les clics sur le plateau
        const rect = this.canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        const col = Math.floor(x / this.cellSize);
        const row = Math.floor(y / this.cellSize);
        
        if (row >= 0 && row < this.gridRows && col >= 0 && col < this.gridCols) {
            if (this.grid[row][col] !== null) {
                const piece = this.detectPiece(row, col);
                
                if (piece.size > 1) {  // Si la pièce est valide (plus d'un bloc), on la retire
                    // Retirer la pièce en mettant ses cases à null
                    for (let coords of piece) {
                        const [r, c] = coords.split(',').map(Number);
                        this.grid[r][c] = null;
                    }
                    
                    // Faire descendre les blocs situés au-dessus de la pièce
                    this.updateGrid(piece);
                    
                    // Tasser le restant du plateau en supprimant les colonnes vides
                    this.removeEmptyColumns();
                    
                    // Rafraîchir le plateau pour répercuter les modifications
                    this.refreshBoard();
                    this.refreshBlocCount(piece);
                    
                    if (this.isGameOver()) {
                        this.ctx.fillStyle = "red";
                        this.ctx.font = "bold 16px Courier";
                        this.ctx.textAlign = "center";
                        this.ctx.fillText("LA PARTIE EST TERMINÉE", this.boardWidth / 2, this.cellSize / 2 + 5);
                    }
                }
            }
        }
    }
    
    detectPiece(row, col) {
        // Détecte tous les blocs connectés de même couleur
        const piece = new Set();
        const color = this.grid[row][col];
        
        const explore = (r, c) => {
            const key = `${r},${c}`;
            if (piece.has(key) || this.grid[r][c] !== color) return;
            
            piece.add(key);
            
            // Directions: haut, bas, gauche, droite
            const directions = [[-1, 0], [1, 0], [0, -1], [0, 1]];
            
            for (let [dr, dc] of directions) {
                const nr = r + dr;
                const nc = c + dc;
                
                if (nr >= 0 && nr < this.gridRows && nc >= 0 && nc < this.gridCols && 
                    this.grid[nr][nc] === color) {
                    explore(nr, nc);
                }
            }
        };
        
        explore(row, col);
        return piece;
    }
    
    updateGrid(piece) {
        // Fait descendre les blocs après suppression d'une pièce
        // Parcourir chaque colonne
        for (let j = 0; j < this.gridCols; j++) {
            // Extraire les blocs non vides de la colonne
            let column = [];
            for (let i = 0; i < this.gridRows; i++) {
                if (this.grid[i][j] !== null) {
                    column.push(this.grid[i][j]);
                }
            }
            
            // Compléter avec null pour atteindre la hauteur du plateau
            column = Array(this.gridRows - column.length).fill(null).concat(column);
            
            // Réinsérer la colonne mise à jour dans la matrice
            for (let i = 0; i < this.gridRows; i++) {
                this.grid[i][j] = column[i];
            }
        }
    }
    
    removeEmptyColumns() {
        // Supprime les colonnes vides et décale les autres
        // Identifier les colonnes non vides
        let nonEmptyColumns = [];
        for (let j = 0; j < this.gridCols; j++) {
            let isEmpty = true;
            for (let i = 0; i < this.gridRows; i++) {
                if (this.grid[i][j] !== null) {
                    isEmpty = false;
                    break;
                }
            }
            if (!isEmpty) {
                nonEmptyColumns.push(j);
            }
        }
        
        // Créer une nouvelle grille avec les colonnes non vides à gauche
        let newGrid = Array(this.gridRows).fill().map(() => Array(this.gridCols).fill(null));
        
        for (let newCol = 0; newCol < nonEmptyColumns.length; newCol++) {
            let oldCol = nonEmptyColumns[newCol];
            for (let i = 0; i < this.gridRows; i++) {
                newGrid[i][newCol] = this.grid[i][oldCol];
            }
        }
        
        this.grid = newGrid;
    }
    
    isGameOver() {
        // Vérifie si la partie est terminée
        // La partie est terminée si le plateau est vide
        let isEmpty = true;
        for (let i = 0; i < this.gridRows; i++) {
            for (let j = 0; j < this.gridCols; j++) {
                if (this.grid[i][j] !== null) {
                    isEmpty = false;
                    break;
                }
            }
            if (!isEmpty) break;
        }
        
        if (isEmpty) return true;
        
        // Ou si toutes les pièces restantes sont de taille 1
        for (let i = 0; i < this.gridRows; i++) {
            for (let j = 0; j < this.gridCols; j++) {
                if (this.grid[i][j] !== null) {
                    const piece = this.detectPiece(i, j);
                    if (piece.size > 1) {
                        return false;
                    }
                }
            }
        }
        
        return true;
    }
    
    reset() {
        // Réinitialise le jeu
        this.initGame();
    }
}

// Initialisation du jeu lorsque la page est chargée
document.addEventListener('DOMContentLoaded', function() {
    const resetButton = document.getElementById('reset-button');
    const game = new Klickety('game-canvas', 'bloc-count-canvas');
    
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            game.reset();
        });
    }
});
