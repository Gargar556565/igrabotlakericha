from enum import Enum


class Cell(Enum):
    EMPTY = " "
    X = "X"
    O = "O"


class TicTacToe:
    LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
        (0, 4, 8), (2, 4, 6),              # diagonals
    ]

    def __init__(self):
        self.board: list[Cell] = [Cell.EMPTY] * 9
        self.current_player: Cell = Cell.X
        self.winner: Cell | None = None
        self.is_draw: bool = False

    # ── helpers ──────────────────────────────────────────────────────────
    @staticmethod
    def _check_line(line: tuple[int, ...], board: list[Cell]) -> Cell | None:
        a, b, c = line
        if (board[a] != Cell.EMPTY
                and board[a] == board[b]
                and board[a] == board[c]):
            return board[a]
        return None

    # ── public API ───────────────────────────────────────────────────────
    def make_move(self, index: int, player: Cell) -> bool:
        """Place mark at *index*.  Returns ``True`` on success."""
        if self.winner or self.is_draw:
            return False
        if not (0 <= index < 9):
            return False
        if self.board[index] != Cell.EMPTY:
            return False

        self.board[index] = player

        # check win
        for line in self.LINES:
            if winner := self._check_line(line, self.board):
                self.winner = winner
                return True

        # check draw
        if Cell.EMPTY not in self.board:
            self.is_draw = True
        return True

    @property
    def status(self) -> str:
        if self.winner:
            sym = "X" if self.winner == Cell.X else "O"
            return f"**Победил {sym}!** \U0001f3c6\n_/new — новая игра_"
        if self.is_draw:
            return "**Ничья!** \U0001f91d\n_/new — новая игра_"
        player_symbol = "X" if self.current_player == Cell.X else "O"
        return f"**Ходит:** {player_symbol}"

    def display_board(self) -> str:
        symbols = [
            "\U0001f7e5" if c == Cell.EMPTY else
            "\u274c" if c == Cell.X else
            "\U00002b55"
            for c in self.board
        ]
        row_sep = "\u2500\u2500\u2500+\u2500\u2500\u2500+\u2500\u2500\u2500\n"
        cells = (f"| {symbols[0]} | {symbols[1]} | {symbols[2]} |\n{row_sep}"
                 f"| {symbols[3]} | {symbols[4]} | {symbols[5]} |\n{row_sep}"
                 f"| {symbols[6]} | {symbols[7]} | {symbols[8]} |")
        return cells

    def reset(self):
        self.board = [Cell.EMPTY] * 9
        self.current_player = Cell.X
        self.winner = None
        self.is_draw = False

    # ── AI (минимакс) ────────────────────────────────────────────────
    def get_best_move(self) -> int:
        """Возвращает лучший ход для бота (играет за O)."""
        best_score = -float('inf')
        move = -1
        for i in range(9):
            if self.board[i] == Cell.EMPTY:
                self.board[i] = Cell.O
                score = self._minimax(False)  # бот максимизирует, игрок минимизирует
                self.board[i] = Cell.EMPTY
                if score > best_score:
                    best_score = score
                    move = i
        return move

    def _minimax(self, is_maximizing: bool) -> int:
        # Проверяем победителя
        winner = None
        for a, b, c in self.LINES:
            if self.board[a] != Cell.EMPTY and self.board[a] == self.board[b] == self.board[c]:
                winner = self.board[a]
                break

        if winner == Cell.O:
            return 10 - 9 * (self.board.count(Cell.EMPTY) // 9 + 1)  # быстрее победить
        if winner == Cell.X:
            return -10 + 9 * (self.board.count(Cell.EMPTY) / 9)  # медленнее проиграть
        if self.is_draw or Cell.EMPTY not in self.board:
            return 0

        if is_maximizing:  # бот (O)
            best = -float('inf')
            for i in range(9):
                if self.board[i] == Cell.EMPTY:
                    self.board[i] = Cell.O
                    best = max(best, self._minimax(False))
                    self.board[i] = Cell.EMPTY
            return best
        else:  # игрок (X)
            best = float('inf')
            for i in range(9):
                if self.board[i] == Cell.EMPTY:
                    self.board[i] = Cell.X
                    best = min(best, self._minimax(True))
                    self.board[i] = Cell.EMPTY
            return best

