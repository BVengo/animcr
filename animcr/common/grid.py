from manim import VGroup, Square, Rectangle, BLACK, rgb_to_color
import numpy as np


class Grid(VGroup):
    cells: list[Square] = []
    border: Rectangle

    data: np.ndarray
    cell_size: float

    cols: int
    rows: int
    width: float
    height: float

    def __init__(self, cell_size: float, data: np.ndarray, **kwargs):
        super().__init__(**kwargs)

        self.cell_size = cell_size
        self.data = data

        self.calculate_sizes()
        self.add_cells()
        self.add_border()

    def calculate_sizes(self):
        self.cols = self.data.shape[1]
        self.rows = self.data.shape[0]

        self.width = self.cell_size * self.cols
        self.height = self.cell_size * self.rows

    def add_cells(self):
        self.cells = []

        # Create a list of all the cells
        for i in range(self.rows):
            for j in range(self.cols):
                val = self.data[i, j]

                # Determine cell color
                cell_color = BLACK if np.isnan(val) else rgb_to_color((val, val, val))

                # Create the cell
                cell = Square(
                    side_length=self.cell_size,
                    fill_color=cell_color,
                    fill_opacity=1,
                    stroke_opacity=0,
                    stroke_width=0
                )

                # Add the cell to the list of cells
                self.cells.append(cell)
                self.add(cell)

        self.arrange_in_grid(rows=self.rows, cols=self.cols, buff=0)

    def get_cell(self, idx: int) -> Square:
        return self.cells[idx]

    def get_cells(self) -> list[Square]:
        return self.cells

    def get_border(self) -> Rectangle:
        return self.border

    def add_border(self):
        self.border = Rectangle(width=self.width, height=self.height, fill_opacity=0, stroke_opacity=1, stroke_width=2)
        self.add(self.border)
