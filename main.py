import tkinter as tk
from tkinter import simpledialog, messagebox, Menu
import random

class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.current_player = 1
        self.red_wins = 0
        self.yellow_wins = 0
        self.red_player = "Red"
        self.yellow_player = "Yellow"
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.ai_active = False
        self.ai_difficulty = "Easy"
        self.create_board()
        self.status_label = tk.Label(root, text="Welcome to Connect Four!", font=("Arial", 12))
        self.status_label.grid(row=6, column=0, columnspan=7)
        self.create_menu()
        self.create_scoreboard()
        self.turn_label = tk.Label(root, text=f"{self.red_player}'s Turn", font=("Arial", 12))
        self.turn_label.grid(row=7, column=0, columnspan=7)
        self.prompt_player_names()

    def create_board(self):
        self.cells = []
        for row in range(6):
            row_cells = []
            for col in range(7):
                cell = tk.Frame(
                    self.root, 
                    width=60, 
                    height=60, 
                    bg='blue', 
                    borderwidth=2, 
                    relief='ridge'
                )
                cell.grid(row=row, column=col, padx=2, pady=2)
                cell.bind("<Button-1>", lambda e, row=row, col=col: self.cell_clicked(row, col))
                row_cells.append(cell)
            self.cells.append(row_cells)

    def create_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        game_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.reset_board)
        game_menu.add_command(label="Reset Game", command=self.reset_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)

        options_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Change Players' Names", command=self.prompt_player_names)
        options_menu.add_command(label="Play Against AI", command=self.play_with_ai)
        options_menu.add_command(label="Switch to Two Players", command=self.switch_to_two_players)

        difficulty_menu = Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="AI Difficulty", menu=difficulty_menu)
        difficulty_menu.add_command(label="Easy", command=lambda: self.set_ai_difficulty("Easy"))
        difficulty_menu.add_command(label="Medium", command=lambda: self.set_ai_difficulty("Medium"))
        difficulty_menu.add_command(label="Hard", command=lambda: self.set_ai_difficulty("Hard"))

        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Game Instructions", command=self.show_instructions)

    def set_ai_difficulty(self, difficulty):
        self.ai_difficulty = difficulty
        messagebox.showinfo("AI Difficulty", f"AI difficulty set to {difficulty}")

    def create_scoreboard(self):
        self.scoreboard = tk.LabelFrame(self.root, text="Scoreboard", font=("Arial", 12))
        self.scoreboard.grid(row=9, column=0, columnspan=7, padx=10, pady=10)
        self.red_win_label = tk.Label(self.scoreboard, text="Red Wins: 0", font=("Arial", 12))
        self.red_win_label.grid(row=0, column=0, padx=5, pady=5)
        self.yellow_win_label = tk.Label(self.scoreboard, text="Yellow Wins: 0", font=("Arial", 12))
        self.yellow_win_label.grid(row=0, column=1, padx=5, pady=5)

    def show_instructions(self):
        instructions = (
            "Connect Four Instructions:\n\n"
            "1. The game is played on a 6x7 grid.\n"
            "2. Players take turns dropping their colored discs from the top into a column.\n"
            "3. The first player to connect four discs vertically, horizontally, or diagonally wins.\n"
            "4. If the board fills up without a winner, the game is a tie.\n\n"
            "Enjoy playing Connect Four!"
        )
        messagebox.showinfo("Instructions", instructions)

    def cell_clicked(self, row, col):
        if self.board[0][col] != 0:
            messagebox.showwarning("Column Full", "This column is already full. Please choose another column.")
            return

        for r in range(5, -1, -1):
            if self.board[r][col] == 0:
                self.board[r][col] = self.current_player
                self.update_gui(r, col)
                if self.check_win(r, col):
                    self.show_winner(r, col)
                elif self.check_tie():
                    messagebox.showinfo("Game Over", "It's a tie!")
                    self.reset_board()
                else:
                    self.current_player = 2 if self.current_player == 1 else 1
                    self.update_turn_label()
                    if self.ai_active and self.current_player == 2:
                        self.root.after(1000, self.ai_move)
                break

    def update_gui(self, row, col):
        color = 'red' if self.board[row][col] == 1 else 'yellow'
        self.cells[row][col].config(bg=color)

    def update_turn_label(self):
        current_turn = self.red_player if self.current_player == 1 else self.yellow_player
        self.turn_label.config(text=f"{current_turn}'s Turn")

    def check_win(self, row, col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            winning_cells = [(row, col)]
            for d in [1, -1]:
                r, c = row + d * dr, col + d * dc
                while 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == self.current_player:
                    count += 1
                    winning_cells.append((r, c))
                    r += d * dr
                    c += d * dc
            if count >= 4:
                self.highlight_winning_cells(winning_cells)
                return True
        return False

    def highlight_winning_cells(self, winning_cells):
        for r, c in winning_cells:
            self.cells[r][c].config(bg='green')

    def check_tie(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

    def show_winner(self, row, col):
        winner = self.red_player if self.current_player == 1 else self.yellow_player
        if self.current_player == 1:
            self.red_wins += 1
            self.red_win_label.config(text=f"Red Wins: {self.red_wins}")
        else:
            self.yellow_wins += 1
            self.yellow_win_label.config(text=f"Yellow Wins: {self.yellow_wins}")
        messagebox.showinfo("Game Over", f"{winner} wins!")
        self.reset_board()

    def reset_game(self):
        self.red_wins = 0
        self.yellow_wins = 0
        self.red_win_label.config(text="Red Wins: 0")
        self.yellow_win_label.config(text="Yellow Wins: 0")
        self.reset_board()

    def reset_board(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        for row in range(6):
            for col in range(7):
                self.cells[row][col].config(bg='blue')
        self.current_player = 1
        self.update_turn_label()

    def prompt_player_names(self):
        self.red_player = simpledialog.askstring("Player Name", "Enter name for Red player:", initialvalue="Red")
        self.yellow_player = simpledialog.askstring("Player Name", "Enter name for Yellow player:", initialvalue="Yellow")
        self.update_turn_label()

    def play_with_ai(self):
        self.ai_active = True
        self.prompt_player_names()
        self.reset_board()

    def switch_to_two_players(self):
        self.ai_active = False
        self.prompt_player_names()
        self.reset_board()

    def ai_move(self):
        if self.ai_difficulty == "Easy":
            self.ai_move_easy()
        elif self.ai_difficulty == "Medium":
            self.ai_move_medium()
        elif self.ai_difficulty == "Hard":
            self.ai_move_hard()

    def ai_move_easy(self):
        valid_columns = [col for col in range(7) if self.board[0][col] == 0]
        if valid_columns:
            chosen_column = random.choice(valid_columns)
            self.cell_clicked(0, chosen_column)

    def ai_move_medium(self):
        for col in range(7):
            if self.board[0][col] == 0:
                for r in range(5, -1, -1):
                    if self.board[r][col] == 0:
                        self.board[r][col] = 2
                        if self.check_win(r, col):
                            self.board[r][col] = 0
                            self.cell_clicked(0, col)
                            return
                        self.board[r][col] = 0
                        break

        for col in range(7):
            if self.board[0][col] == 0:
                for r in range(5, -1, -1):
                    if self.board[r][col] == 0:
                        self.board[r][col] = 1
                        if self.check_win(r, col):
                            self.board[r][col] = 0
                            self.cell_clicked(0, col)
                            return
                        self.board[r][col] = 0
                        break

        self.ai_move_easy()

    def ai_move_hard(self):
        best_score = -float('inf')
        best_col = None

        for col in range(7):
            if self.board[0][col] == 0:
                for r in range(5, -1, -1):
                    if self.board[r][col] == 0:
                        self.board[r][col] = 2
                        score = self.minimax(self.board, 4, -float('inf'), float('inf'), False)
                        self.board[r][col] = 0
                        if score > best_score:
                            best_score = score
                            best_col = col
                        break

        if best_col is not None:
            self.cell_clicked(0, best_col)

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0 or self.check_tie() or self.check_win_state(1) or self.check_win_state(2):
            return self.evaluate_board(board)

        if is_maximizing:
            max_eval = -float('inf')
            for col in range(7):
                if board[0][col] == 0:
                    for r in range(5, -1, -1):
                        if board[r][col] == 0:
                            board[r][col] = 2
                            eval = self.minimax(board, depth-1, alpha, beta, False)
                            board[r][col] = 0
                            max_eval = max(max_eval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
            return max_eval
        else:
            min_eval = float('inf')
            for col in range(7):
                if board[0][col] == 0:
                    for r in range(5, -1, -1):
                        if board[r][col] == 0:
                            board[r][col] = 1
                            eval = self.minimax(board, depth-1, alpha, beta, True)
                            board[r][col] = 0
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break
            return min_eval

    def evaluate_board(self, board):
        score = 0

        for row in range(6):
            for col in range(4):
                window = [board[row][col+i] for i in range(4)]
                score += self.evaluate_window(window)

        for col in range(7):
            for row in range(3):
                window = [board[row+i][col] for i in range(4)]
                score += self.evaluate_window(window)

        for row in range(3):
            for col in range(4):
                window = [board[row+i][col+i] for i in range(4)]
                score += self.evaluate_window(window)

        for row in range(3):
            for col in range(4):
                window = [board[row+3-i][col+i] for i in range(4)]
                score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window):
        score = 0
        opp_piece = 1 if self.current_player == 2 else 2

        if window.count(self.current_player) == 4:
            score += 100
        elif window.count(self.current_player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(self.current_player) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def check_win_state(self, player):
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == player:
                    if self.check_win(row, col):
                        return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect Four")
    game = ConnectFour(root)
    root.mainloop()
