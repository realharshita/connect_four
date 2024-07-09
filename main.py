import tkinter as tk
from tkinter import simpledialog, messagebox

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
        reset_button = tk.Button(root, text="Reset Game", command=self.reset_game)
        reset_button.grid(row=7, column=0, columnspan=3)
        new_game_button = tk.Button(root, text="New Game", command=self.reset_board)
        new_game_button.grid(row=7, column=4, columnspan=3)
        self.red_win_label = tk.Label(root, text="Red Wins: 0", font=("Arial", 12))
        self.red_win_label.grid(row=8, column=0, columnspan=3)
        self.yellow_win_label = tk.Label(root, text="Yellow Wins: 0", font=("Arial", 12))
        self.yellow_win_label.grid(row=8, column=4, columnspan=3)
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

    def cell_clicked(self, row, col):
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
                    self.status_label.config(text=f"{self.red_player}'s Turn" if self.current_player == 2 else f"{self.yellow_player}'s Turn")
                self.current_player = 3 - self.current_player
                break

    def update_gui(self, row, col):
        color = 'red' if self.board[row][col] == 1 else 'yellow'
        self.cells[row][col].config(bg=color)

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
        self.status_label.config(text=f"{self.red_player}'s Turn")

    def prompt_player_names(self):
        self.red_player = simpledialog.askstring("Player Name", "Enter name for Red player:", initialvalue="Red")
        self.yellow_player = simpledialog.askstring("Player Name", "Enter name for Yellow player:", initialvalue="Yellow")
        self.status_label.config(text=f"{self.red_player}'s Turn")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect Four")
    game = ConnectFour(root)
    root.mainloop()
