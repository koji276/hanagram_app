import tkinter as tk
import numpy as np

class TriangleBoardApp:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=600, height=600, bg='white')
        self.canvas.pack()

        self.board_structure = [
            ['N', 'N', 'N', 'U', 'D', 'U', 'N', 'N', 'N'],
            ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
            ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
            ['U', 'D', 'U', 'D', 'U', 'D', 'U', 'D', 'U'],
            ['D', 'U', 'D', 'U', 'D', 'U', 'D', 'U', 'D'],
            ['N', 'N', 'N', 'D', 'U', 'D', 'N', 'N', 'N'],
        ]

        self.cell_size = 40
        self.height = np.sqrt(3) / 2 * self.cell_size
        self.selected_cell = None
        self.board_values = [[None]*9 for _ in range(6)]

        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        root.bind("<Key>", self.on_key)

    def draw_board(self):
        self.canvas.delete("all")
        for row_idx, row in enumerate(self.board_structure):
            for col_idx, cell in enumerate(row):
                if cell != 'N':
                    x_offset = col_idx * (self.cell_size / 2) + 100
                    y_offset = row_idx * (self.height) + 50
                    self.draw_triangle(x_offset, y_offset, direction=cell, row=row_idx, col=col_idx)

    def draw_triangle(self, x, y, direction, row, col):
        if direction == 'U':
            points = [x, y + self.height, x + self.cell_size / 2, y, x + self.cell_size, y + self.height]
        else:
            points = [x, y, x + self.cell_size / 2, y + self.height, x + self.cell_size, y]

        fill_color = 'lightblue' if self.selected_cell == (row, col) else 'white'
        self.canvas.create_polygon(points, outline='black', fill=fill_color, tags=f"{row},{col}")

        value = self.board_values[row][col]
        if value is not None:
            self.canvas.create_text(x + self.cell_size / 2, y + self.height / 2, text=str(value), font=('Arial', 16))

    def on_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(item)
        if tags:
            row, col = map(int, tags[0].split(','))
            self.selected_cell = (row, col)
            self.draw_board()

    def on_key(self, event):
        if self.selected_cell and event.char in '0123456789':
            row, col = self.selected_cell
            self.board_values[row][col] = int(event.char)
            self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Triangle Board App")
    app = TriangleBoardApp(root)
    root.mainloop()
