import tkinter as tk

class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.current_player = 1
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.create_board()

    def create_board(self):
        for row in range(6):
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

    def cell_clicked(self, row, col):
        for r in range(5, -1, -1):
            if self.board[r][col] == 0:
                self.board[r][col] = self.current_player
                self.update_gui(r, col)
                self.current_player = 3 - self.current_player  # Switch player
                break

    def update_gui(self, row, col):
        color = 'red' if self.current_player == 1 else 'yellow'
        cell = tk.Frame(
            self.root, 
            width=60, 
            height=60, 
            bg=color, 
            borderwidth=2, 
            relief='ridge'
        )
        cell.grid(row=row, column=col)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect Four")
    game = ConnectFour(root)
    root.mainloop()
