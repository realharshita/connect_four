import tkinter as tk
from tkinter import messagebox

class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.current_player = 1
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.create_board()
        self.turn_label = tk.Label(root, text="Red's Turn", font=("Arial", 16))
        self.turn_label.grid(row=6, column=0, columnspan=7)
        reset_button = tk.Button(root, text="Reset Game", command=self.reset_game)
        reset_button.grid(row=7, column=0, columnspan=7)

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
                cell.grid(row=row, column=col)
                cell.bind("<Button-1>", lambda e, row=row, col=col: self.cell_clicked(row, col))
                row_cells.append(cell)
            self.cells.append(row_cells)

    def cell_clicked(self, row, col):
        for r in range(5, -1, -1):
            if self.board[r][col] == 0:
                self.board[r][col] = self.current_player
                self.update_gui(r, col)
                if self.check_win(r, col):
                    self.show_winner()
                self.current_player = 3 - self.current_player
                self.turn_label.config(text="Yellow's Turn" if self.current_player == 2 else "Red's Turn")
                break

    def update_gui(self, row, col):
        color = 'red' if self.board[row][col] == 1 else 'yellow'
        self.cells[row][col].config(bg=color)

    def check_win(self, row, col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for d in [1, -1]:
                r, c = row + d * dr, col + d * dc
                while 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == self.current_player:
                    count += 1
                    r += d * dr
                    c += d * dc
            if count >= 4:
                return True
        return False

    def show_winner(self):
        winner = 'Red' if self.current_player == 1 else 'Yellow'
        messagebox.showinfo("Game Over", f"{winner} wins!")
        self.reset_game()

    def reset_game(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        for row in range(6):
            for col in range(7):
                self.cells[row][col].config(bg='blue')
        self.current_player = 1
        self.turn_label.config(text="Red's Turn")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect Four")
    game = ConnectFour(root)
    root.mainloop()
