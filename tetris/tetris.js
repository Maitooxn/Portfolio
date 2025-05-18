// Tetris Game Implementation
document.addEventListener('DOMContentLoaded', function() {
    // Canvas setup
    const canvas = document.getElementById('tetris-canvas');
    const ctx = canvas.getContext('2d');
    const nextPieceCanvas = document.getElementById('next-piece-canvas');
    const nextPieceCtx = nextPieceCanvas.getContext('2d');
    
    // Game elements
    const scoreElement = document.getElementById('score');
    const levelElement = document.getElementById('level');
    const linesElement = document.getElementById('lines');
    const startButton = document.getElementById('start-button');
    const resetButton = document.getElementById('reset-button');
    const gameModeSelect = document.getElementById('game-mode');
    
    // Game constants
    const COLS = 12;
    const ROWS = 24;
    const BLOCK_SIZE = canvas.width / COLS;
    const COLORS = [
        null,
        '#FF9800', // orange
        '#03A9F4', // lightblue
        '#F44336', // lightcoral
        '#9C27B0', // lavender
        '#4CAF50', // lightgreen
        '#FFEB3B'  // beige
    ];
    
    // Tetromino shapes
    const SHAPES = {
        I: [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        J: [
            [2, 0, 0],
            [2, 2, 2],
            [0, 0, 0]
        ],
        L: [
            [0, 0, 3],
            [3, 3, 3],
            [0, 0, 0]
        ],
        O: [
            [4, 4],
            [4, 4]
        ],
        S: [
            [0, 5, 5],
            [5, 5, 0],
            [0, 0, 0]
        ],
        T: [
            [0, 6, 0],
            [6, 6, 6],
            [0, 0, 0]
        ],
        Z: [
            [7, 7, 0],
            [0, 7, 7],
            [0, 0, 0]
        ]
    };
    
    // Game variables
    let board = createBoard();
    let piece = null;
    let nextPiece = null;
    let score = 0;
    let level = 1;
    let lines = 0;
    let dropCounter = 0;
    let dropInterval = 1000;
    let lastTime = 0;
    let gameOver = false;
    let paused = false;
    let gameActive = false;
    let gameMode = 'standard';
    let animationId = null;
    
    // Create game board
    function createBoard() {
        const board = [];
        for (let row = 0; row < ROWS; row++) {
            board.push(new Array(COLS).fill(0));
        }
        return board;
    }
    
    // Create a new tetromino
    function createPiece(type) {
        const shape = SHAPES[type];
        return {
            shape,
            pos: {
                x: Math.floor(COLS / 2) - Math.floor(shape[0].length / 2),
                y: 0
            },
            type
        };
    }
    
    // Get random tetromino
    function getRandomPiece() {
        const pieces = 'IJLOSTZ';
        const randomPiece = pieces[Math.floor(Math.random() * pieces.length)];
        return createPiece(randomPiece);
    }
    
    // Draw a single block
    function drawBlock(x, y, color) {
        ctx.fillStyle = color;
        ctx.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 1;
        ctx.strokeRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
        
        // Add 3D effect
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.beginPath();
        ctx.moveTo(x * BLOCK_SIZE, y * BLOCK_SIZE);
        ctx.lineTo((x + 1) * BLOCK_SIZE, y * BLOCK_SIZE);
        ctx.lineTo(x * BLOCK_SIZE, (y + 1) * BLOCK_SIZE);
        ctx.fill();
        
        ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        ctx.beginPath();
        ctx.moveTo((x + 1) * BLOCK_SIZE, y * BLOCK_SIZE);
        ctx.lineTo((x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE);
        ctx.lineTo(x * BLOCK_SIZE, (y + 1) * BLOCK_SIZE);
        ctx.fill();
    }
    
    // Draw the board
    function drawBoard() {
        ctx.fillStyle = '#1a1a2e';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw grid lines
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        ctx.lineWidth = 1;
        
        // Vertical lines
        for (let x = 0; x <= COLS; x++) {
            ctx.beginPath();
            ctx.moveTo(x * BLOCK_SIZE, 0);
            ctx.lineTo(x * BLOCK_SIZE, canvas.height);
            ctx.stroke();
        }
        
        // Horizontal lines
        for (let y = 0; y <= ROWS; y++) {
            ctx.beginPath();
            ctx.moveTo(0, y * BLOCK_SIZE);
            ctx.lineTo(canvas.width, y * BLOCK_SIZE);
            ctx.stroke();
        }
        
        // Draw blocks
        for (let y = 0; y < ROWS; y++) {
            for (let x = 0; x < COLS; x++) {
                if (board[y][x]) {
                    drawBlock(x, y, COLORS[board[y][x]]);
                }
            }
        }
    }
    
    // Draw the current piece
    function drawPiece() {
        if (!piece) return;
        
        piece.shape.forEach((row, y) => {
            row.forEach((value, x) => {
                if (value) {
                    drawBlock(piece.pos.x + x, piece.pos.y + y, COLORS[value]);
                }
            });
        });
    }
    
    // Draw the next piece preview
    function drawNextPiece() {
        if (!nextPiece) return;
        
        // Clear the canvas
        nextPieceCtx.fillStyle = '#1a1a2e';
        nextPieceCtx.fillRect(0, 0, nextPieceCanvas.width, nextPieceCanvas.height);
        
        // Calculate center position
        const blockSize = 25;
        const shapeWidth = nextPiece.shape[0].length * blockSize;
        const shapeHeight = nextPiece.shape.length * blockSize;
        const startX = (nextPieceCanvas.width - shapeWidth) / 2;
        const startY = (nextPieceCanvas.height - shapeHeight) / 2;
        
        // Draw the next piece
        nextPiece.shape.forEach((row, y) => {
            row.forEach((value, x) => {
                if (value) {
                    // Draw block
                    nextPieceCtx.fillStyle = COLORS[value];
                    nextPieceCtx.fillRect(startX + x * blockSize, startY + y * blockSize, blockSize, blockSize);
                    
                    // Draw border
                    nextPieceCtx.strokeStyle = '#000';
                    nextPieceCtx.lineWidth = 1;
                    nextPieceCtx.strokeRect(startX + x * blockSize, startY + y * blockSize, blockSize, blockSize);
                    
                    // Add 3D effect
                    nextPieceCtx.fillStyle = 'rgba(255, 255, 255, 0.3)';
                    nextPieceCtx.beginPath();
                    nextPieceCtx.moveTo(startX + x * blockSize, startY + y * blockSize);
                    nextPieceCtx.lineTo(startX + (x + 1) * blockSize, startY + y * blockSize);
                    nextPieceCtx.lineTo(startX + x * blockSize, startY + (y + 1) * blockSize);
                    nextPieceCtx.fill();
                    
                    nextPieceCtx.fillStyle = 'rgba(0, 0, 0, 0.2)';
                    nextPieceCtx.beginPath();
                    nextPieceCtx.moveTo(startX + (x + 1) * blockSize, startY + y * blockSize);
                    nextPieceCtx.lineTo(startX + (x + 1) * blockSize, startY + (y + 1) * blockSize);
                    nextPieceCtx.lineTo(startX + x * blockSize, startY + (y + 1) * blockSize);
                    nextPieceCtx.fill();
                }
            });
        });
    }
    
    // Check for collision
    function collide() {
        if (!piece) return false;
        
        for (let y = 0; y < piece.shape.length; y++) {
            for (let x = 0; x < piece.shape[y].length; x++) {
                if (piece.shape[y][x] !== 0 &&
                    (board[piece.pos.y + y] === undefined ||
                     board[piece.pos.y + y][piece.pos.x + x] === undefined ||
                     board[piece.pos.y + y][piece.pos.x + x] !== 0)) {
                    return true;
                }
            }
        }
        return false;
    }
    
    // Merge the piece with the board
    function merge() {
        if (!piece) return;
        
        piece.shape.forEach((row, y) => {
            row.forEach((value, x) => {
                if (value) {
                    board[piece.pos.y + y][piece.pos.x + x] = value;
                }
            });
        });
    }
    
    // Move the piece
    function movePiece(dir) {
        piece.pos.x += dir;
        if (collide()) {
            piece.pos.x -= dir;
            return false;
        }
        return true;
    }
    
    // Drop the piece
    function dropPiece() {
        piece.pos.y++;
        if (collide()) {
            piece.pos.y--;
            merge();
            resetPiece();
            removeLines();
            return false;
        }
        return true;
    }
    
    // Hard drop the piece
    function hardDrop() {
        while (dropPiece()) {
            // Keep dropping
        }
    }
    
    // Rotate the piece
    function rotatePiece(dir) {
        const pos = piece.pos.x;
        let offset = 1;
        rotate(piece.shape, dir);
        
        // Wall kick
        while (collide()) {
            piece.pos.x += offset;
            offset = -(offset + (offset > 0 ? 1 : -1));
            if (offset > piece.shape[0].length) {
                rotate(piece.shape, -dir);
                piece.pos.x = pos;
                return;
            }
        }
    }
    
    // Rotate a matrix
    function rotate(matrix, dir) {
        // Transpose the matrix
        for (let y = 0; y < matrix.length; y++) {
            for (let x = 0; x < y; x++) {
                [matrix[x][y], matrix[y][x]] = [matrix[y][x], matrix[x][y]];
            }
        }
        
        // Reverse each row to get a rotated matrix
        if (dir > 0) {
            matrix.forEach(row => row.reverse());
        } else {
            matrix.reverse();
        }
    }
    
    // Reset the piece
    function resetPiece() {
        // Check if game over
        if (piece.pos.y === 0) {
            showGameOver();
            return;
        }
        
        // Set the next piece as current
        piece = nextPiece;
        nextPiece = getRandomPiece();
        drawNextPiece();
    }
    
    // Remove completed lines
    function removeLines() {
        let linesCleared = 0;
        
        outer: for (let y = ROWS - 1; y >= 0; y--) {
            for (let x = 0; x < COLS; x++) {
                if (board[y][x] === 0) {
                    continue outer;
                }
            }
            
            // Remove the line
            const row = board.splice(y, 1)[0].fill(0);
            board.unshift(row);
            y++;
            
            linesCleared++;
        }
        
        // Add pourrissement blocks if in that mode
        if (gameMode === 'pourrissement' && linesCleared > 0) {
            addPourissementBlocks(linesCleared);
        }
        
        // Update score
        if (linesCleared > 0) {
            // Scoring system: 100 * level * lines^2
            score += 100 * level * Math.pow(linesCleared, 2);
            lines += linesCleared;
            
            // Level up every 10 lines
            if (Math.floor(lines / 10) > level - 1) {
                level = Math.floor(lines / 10) + 1;
                // Increase speed with level
                dropInterval = Math.max(100, 1000 - (level - 1) * 100);
            }
            
            updateScore();
        }
    }
    
    // Add pourrissement blocks
    function addPourissementBlocks(linesCleared) {
        // Add random blocks at the bottom
        const newRow = new Array(COLS).fill(0);
        const blockCount = Math.min(COLS - 3, linesCleared * 2); // Ensure there's always a path
        
        // Add random blocks
        for (let i = 0; i < blockCount; i++) {
            let x;
            do {
                x = Math.floor(Math.random() * COLS);
            } while (newRow[x] !== 0);
            
            newRow[x] = Math.floor(Math.random() * 6) + 1; // Random color
        }
        
        // Add the new row at the bottom
        board.push(newRow);
        board.shift();
    }
    
    // Update score display
    function updateScore() {
        scoreElement.textContent = score;
        levelElement.textContent = level;
        linesElement.textContent = lines;
    }
    
    // Reset the game
    function resetGame() {
        // Reset game variables
        board = createBoard();
        score = 0;
        level = 1;
        lines = 0;
        dropCounter = 0;
        dropInterval = 1000;
        gameOver = false;
        paused = false;
        
        // Update display
        updateScore();
        
        // Create new pieces
        piece = getRandomPiece();
        nextPiece = getRandomPiece();
        
        // Hide game over overlay
        const gameOverOverlay = document.querySelector('.game-over-overlay');
        if (gameOverOverlay) {
            gameOverOverlay.classList.remove('active');
        }
        
        // Hide pause overlay
        const pauseOverlay = document.querySelector('.pause-overlay');
        if (pauseOverlay) {
            pauseOverlay.classList.remove('active');
        }
    }
    
    // Show game over
    function showGameOver() {
        gameOver = true;
        gameActive = false;
        
        // Create game over overlay if it doesn't exist
        let gameOverOverlay = document.querySelector('.game-over-overlay');
        if (!gameOverOverlay) {
            gameOverOverlay = document.createElement('div');
            gameOverOverlay.className = 'game-over-overlay';
            
            const gameOverText = document.createElement('div');
            gameOverText.className = 'game-over-text';
            gameOverText.textContent = 'GAME OVER';
            
            const finalScore = document.createElement('div');
            finalScore.className = 'final-score';
            
            const restartButton = document.createElement('button');
            restartButton.className = 'btn btn-primary';
            restartButton.textContent = 'Rejouer';
            restartButton.addEventListener('click', function() {
                resetGame();
                startGame();
            });
            
            gameOverOverlay.appendChild(gameOverText);
            gameOverOverlay.appendChild(finalScore);
            gameOverOverlay.appendChild(restartButton);
            
            document.getElementById('tetris-canvas-container').appendChild(gameOverOverlay);
        }
        
        // Update final score
        const finalScore = gameOverOverlay.querySelector('.final-score');
        finalScore.textContent = `Score final: ${score}`;
        
        // Show overlay
        gameOverOverlay.classList.add('active');
        
        // Update button text
        startButton.textContent = 'Démarrer';
    }
    
    // Toggle pause
    function togglePause() {
        if (gameOver) return;
        
        paused = !paused;
        
        // Create pause overlay if it doesn't exist
        let pauseOverlay = document.querySelector('.pause-overlay');
        if (!pauseOverlay) {
            pauseOverlay = document.createElement('div');
            pauseOverlay.className = 'pause-overlay';
            
            const pauseText = document.createElement('div');
            pauseText.className = 'pause-text';
            pauseText.textContent = 'PAUSE';
            
            const resumeText = document.createElement('div');
            resumeText.className = 'resume-text';
            resumeText.textContent = 'Appuyez sur P pour reprendre';
            
            pauseOverlay.appendChild(pauseText);
            pauseOverlay.appendChild(resumeText);
            
            document.getElementById('tetris-canvas-container').appendChild(pauseOverlay);
        }
        
        // Toggle overlay
        if (paused) {
            pauseOverlay.classList.add('active');
            startButton.textContent = 'Reprendre';
        } else {
            pauseOverlay.classList.remove('active');
            startButton.textContent = 'Pause';
        }
    }
    
    // Start the game
    function startGame() {
        if (gameActive) {
            // If game is active, toggle pause
            togglePause();
            return;
        }
        
        // Reset and start
        resetGame();
        gameActive = true;
        startButton.textContent = 'Pause';
        
        // Get game mode
        gameMode = gameModeSelect.value;
        
        // Start game loop
        if (animationId) {
            cancelAnimationFrame(animationId);
        }
        lastTime = 0;
        update();
    }
    
    // Game loop
    function update(time = 0) {
        if (gameOver) {
            return;
        }
        
        const deltaTime = time - lastTime;
        lastTime = time;
        
        if (!paused) {
            dropCounter += deltaTime;
            if (dropCounter > dropInterval) {
                dropPiece();
                dropCounter = 0;
            }
            
            drawBoard();
            drawPiece();
        }
        
        animationId = requestAnimationFrame(update);
    }
    
    // Handle keyboard input
    document.addEventListener('keydown', event => {
        if (gameOver) return;
        
        // Pause
        if (event.key === 'p' || event.key === 'P') {
            if (gameActive) {
                togglePause();
            }
            return;
        }
        
        if (paused) return;
        
        switch (event.key) {
            case 'ArrowLeft':
                event.preventDefault();
                movePiece(-1);
                break;
            case 'ArrowRight':
                event.preventDefault();
                movePiece(1);
                break;
            case 'ArrowDown':
                event.preventDefault();
                dropPiece();
                break;
            case 'ArrowUp':
                event.preventDefault();
                rotatePiece(1);
                break;
            case ' ':
                event.preventDefault();
                hardDrop();
                break;
        }
    });
    
    // Event listeners
    startButton.addEventListener('click', startGame);
    
    resetButton.addEventListener('click', function() {
        resetGame();
        if (gameActive) {
            startGame();
        }
    });
    
    gameModeSelect.addEventListener('change', function() {
        gameMode = this.value;
        if (gameActive) {
            resetGame();
            startGame();
        }
    });
    
    // Initialize game
    drawBoard();
    drawNextPiece();
    
    // Create game overlays
    const canvasContainer = document.getElementById('tetris-canvas-container');
    
    // Game over overlay
    const gameOverOverlay = document.createElement('div');
    gameOverOverlay.className = 'game-over-overlay';
    
    const gameOverText = document.createElement('div');
    gameOverText.className = 'game-over-text';
    gameOverText.textContent = 'GAME OVER';
    
    const finalScore = document.createElement('div');
    finalScore.className = 'final-score';
    finalScore.textContent = 'Score final: 0';
    
    const restartButton = document.createElement('button');
    restartButton.className = 'btn btn-primary';
    restartButton.textContent = 'Rejouer';
    restartButton.addEventListener('click', function() {
        resetGame();
        startGame();
    });
    
    gameOverOverlay.appendChild(gameOverText);
    gameOverOverlay.appendChild(finalScore);
    gameOverOverlay.appendChild(restartButton);
    
    canvasContainer.appendChild(gameOverOverlay);
    
    // Pause overlay
    const pauseOverlay = document.createElement('div');
    pauseOverlay.className = 'pause-overlay';
    
    const pauseText = document.createElement('div');
    pauseText.className = 'pause-text';
    pauseText.textContent = 'PAUSE';
    
    const resumeText = document.createElement('div');
    resumeText.className = 'resume-text';
    resumeText.textContent = 'Appuyez sur P pour reprendre';
    
    pauseOverlay.appendChild(pauseText);
    pauseOverlay.appendChild(resumeText);
    
    canvasContainer.appendChild(pauseOverlay);
});
