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

        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Game Instructions", command=self.show_instructions)

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
                    self.update_turn_label()
                    if self.current_player == 2 and self.ai_active:
                        self.ai_move()
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

    def ai_move(self):
        # Basic AI: Randomly choose a valid column
        valid_columns = [col for col in range(7) if self.board[0][col] == 0]
        chosen_column = random.choice(valid_columns)
        self.cell_clicked(0, chosen_column)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect Four")
    game = ConnectFour(root)
    root.mainloop()
