const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// ── Состояние игры ──
let gameState = Array(9).fill(null);  // null | 'X' | 'O'
let currentPlayer = 'X';  // X — игрок, O — бот
let gameActive = false;
let scores = { player: 0, draw: 0, bot: 0 };

// ── DOM элементы ──
const boardEl = document.getElementById('board');
const statusEl = document.getElementById('status');
const newGameBtn = document.getElementById('newGameBtn');
const playerNameEl = document.getElementById('playerName');

// ── Инициализация пользователя ──
if (tg.initDataUnsafe.user) {
    const user = tg.initDataUnsafe.user;
    const name = [user.first_name, user.last_name].filter(Boolean).join(' ');
    playerNameEl.textContent = name || 'Игрок';
}

// ── Создание доски ──
function createBoard() {
    boardEl.innerHTML = '';
    for (let i = 0; i < 9; i++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.index = i;
        cell.addEventListener('click', () => onCellClick(i));
        boardEl.appendChild(cell);
    }
}

// ── Отображение доски ──
function renderBoard() {
    const cells = document.querySelectorAll('.cell');
    cells.forEach((cell, i) => {
        cell.textContent = gameState[i] === 'X' ? '❌' : gameState[i] === 'O' ? '⭕' : '';
        cell.classList.toggle('taken', gameState[i] !== null);
    });
}

// ── Показать статус ──
function setStatus(text, emoji = '') {
    statusEl.textContent = text;
}

// ── Показать/скрыть элементы ──
function showBoard() {
    boardEl.classList.remove('hidden');
    newGameBtn.classList.remove('hidden');
}

function hideBoard() {
    boardEl.classList.add('hidden');
    newGameBtn.classList.add('hidden');
}

// ── Обновить счёт ──
function updateScore() {
    document.getElementById('playerScore').textContent = scores.player;
    document.getElementById('drawScore').textContent = scores.draw;
    document.getElementById('botScore').textContent = scores.bot;
}

// ── Клик по ячейке (ход игрока) ──
function onCellClick(index) {
    if (!gameActive || gameState[index] !== null || currentPlayer !== 'X') return;

    makeMove(index, 'X');

    if (!gameActive) return;

    // Ход бота с небольшой задержкой для реалистичности
    setStatus('🤖 Бот думает...');
    setTimeout(() => {
        const botMove = getBestMove();
        if (botMove !== -1) {
            makeMove(botMove, 'O');
        }
    }, 400);
}

// ── Сделать ход ──
function makeMove(index, player) {
    gameState[index] = player;
    renderBoard();

    // Вибрация при ходе
    if (tg.HapticFeedback) {
        tg.HapticFeedback.impactOccurred('light');
    }

    // Проверка результата
    const winner = checkWinner();
    if (winner) {
        gameActive = false;
        if (winner === 'X') {
            scores.player++;
            setStatus('🎉 **Вы победили!**', 'player');
            updateScore();
        } else {
            scores.bot++;
            setStatus('🤖 **Я победил!** Не расстраивайтесь!', 'bot');
            updateScore();
        }
        newGameBtn.classList.remove('hidden');
    } else if (gameState.every(c => c !== null)) {
        gameActive = false;
        scores.draw++;
        setStatus('🤝 **Ничья!** Хорошая игра.', 'draw');
        updateScore();
        newGameBtn.classList.remove('hidden');
    } else {
        currentPlayer = player === 'X' ? 'O' : 'X';
        if (currentPlayer === 'X') {
            setStatus('➡️ **Ваш ход!** Нажмите на свободную клетку.');
        }
    }

    // Если игра активна — показать доску
    if (gameActive) showBoard();
}

// ── Проверка победителя ──
const WIN_LINES = [
    [0,1,2],[3,4,5],[6,7,8],  // rows
    [0,3,6],[1,4,7],[2,5,8],  // cols
    [0,4,8],[2,4,6]           // diagonals
];

function checkWinner() {
    for (const [a, b, c] of WIN_LINES) {
        if (gameState[a] && gameState[a] === gameState[b] && gameState[a] === gameState[c]) {
            return gameState[a];
        }
    }
    return null;
}

// ── AI — Минимакс (бот играет за O) ──
function getBestMove() {
    let bestScore = -Infinity;
    let move = -1;

    for (let i = 0; i < 9; i++) {
        if (gameState[i] === null) {
            gameState[i] = 'O';
            const score = minimax(false);
            gameState[i] = null;
            if (score > bestScore) {
                bestScore = score;
                move = i;
            }
        }
    }
    return move;
}

function minimax(isMaximizing) {
    const winner = checkWinner();
    if (winner === 'O') return 10 + gameState.filter(c => c === null).length;
    if (winner === 'X') return -10 - gameState.filter(c => c === null).length;
    if (gameState.every(c => c !== null)) return 0;

    if (isMaximizing) {  // бот (O)
        let best = -Infinity;
        for (let i = 0; i < 9; i++) {
            if (gameState[i] === null) {
                gameState[i] = 'O';
                best = Math.max(best, minimax(false));
                gameState[i] = null;
            }
        }
        return best;
    } else {  // игрок (X)
        let best = Infinity;
        for (let i = 0; i < 9; i++) {
            if (gameState[i] === null) {
                gameState[i] = 'X';
                best = Math.min(best, minimax(true));
                gameState[i] = null;
            }
        }
        return best;
    }
}

// ── Новая игра ──
function newGame() {
    gameState = Array(9).fill(null);
    currentPlayer = 'X';
    gameActive = true;

    createBoard();
    showBoard();
    setStatus('➡️ **Ваш ход!** Нажмите на свободную клетку.');

    if (tg.HapticFeedback) {
        tg.HapticFeedback.notificationOccurred('success');
    }
}

newGameBtn.addEventListener('click', newGame);

// ── Показать доску сразу при загрузке, если есть активная игра ──
showBoard();
