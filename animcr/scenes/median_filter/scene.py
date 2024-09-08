from manim import *
import numpy as np
from scipy.ndimage import median_filter
from animcr.assetmanager import AssetManager
from animcr.common import Grid


class MedianFilterScene(Scene):
    """
    Applies a median filter to a grayscale image and animates the process.
    """
    IMAGE_PATH = "cr_example.fits"
    KERNEL_SIZE = 3  # Size of the kernel for median filter
    CELL_SIZE = 0.25

    initial_dataset: np.ndarray
    convolved_dataset: np.ndarray
    kernel_dataset: np.ndarray

    data_grid: Grid
    median_grid: Grid
    kernel_grid: Grid
    shifting_square: Square

    def setup(self):
        self.setup_datasets()

    def construct(self):
        self.add_grids()
        self.add_shifting_square()

        # Fade in kernel grid
        self.play(FadeIn(self.kernel_grid), run_time=0.5)

        # for kernel_pos in range(self.initial_dataset.size):
        kernel_pos = 0
        self.shifting_square.move_to(self.kernel_grid.get_cell(4))  # Place on the center of the kernel

        # Set the (hidden) fill color of the kernel
        self.set_kernel_cell_colors(kernel_pos)

        # Change color over 2 seconds to fill in the outer-edges of the kernel
        self.play(AnimationGroup(*[
            cell.animate.set_fill(opacity=1) for cell in self.kernel_grid.get_cells()
        ]), run_time=2.0)

        # Set the (hidden) shifting square to the median cell color
        median_color = self.median_grid.get_cell(kernel_pos).get_fill_color()
        self.shifting_square.set_fill(median_color)

        # Fade the shifting square in
        self.play(self.shifting_square.animate.set_opacity(1), run_time=1.0)

        self.wait(.2)

        # Move the shifting square across to the next index

        # 'Recolor' the cell in the median grid by making it non-transparent

        # Fade out the shifting square

        # Move the kernel onto the next cell while fading the cell fills

        self.wait(2)

    def setup_datasets(self):
        # Load the datasets, clip for visibility, and normalise
        self.initial_dataset = AssetManager.get_image(self.IMAGE_PATH)
        self.convolved_dataset = median_filter(self.initial_dataset, size=self.KERNEL_SIZE, mode="nearest")

        # Normalise to 255
        max_value = np.max(self.initial_dataset)
        self.initial_dataset = (self.initial_dataset / max_value) * 255
        self.convolved_dataset = (self.convolved_dataset / max_value) * 255

        # Bound to min 0 for visibility
        self.initial_dataset = np.clip(self.initial_dataset, 0, a_max=np.inf)
        self.convolved_dataset = np.clip(self.convolved_dataset, 0, a_max=np.inf)

        # Create empty kernel
        self.kernel_dataset = np.zeros((self.KERNEL_SIZE, self.KERNEL_SIZE))

    def add_grids(self):
        self.data_grid = self.add_grid(self.initial_dataset, LEFT)
        self.median_grid = self.add_grid(self.convolved_dataset, RIGHT)
        self.kernel_grid = self.add_grid(self.kernel_dataset).move_to(self.data_grid.get_cell(0))

        for cell in self.data_grid.get_cells():
            cell.set_stroke(color=RED, width=1, opacity=.1)

        for cell in self.median_grid.get_cells():
            cell.set_stroke(color=RED, width=1, opacity=.1)

        for i, cell in enumerate(self.kernel_grid.get_cells()):
            cell.set_stroke(color=RED, width=1, opacity=1)

        self.add(self.kernel_grid)

    def add_grid(self, dataset: np.ndarray, side: np.ndarray | None = None):
        grid = Grid(cell_size=self.CELL_SIZE, data=dataset)

        if side is not None:
            grid.shift(side * (grid.width / 2 + 0.5))

        self.add(grid)

        return grid

    def add_shifting_square(self):
        self.shifting_square = Square(
            side_length=self.CELL_SIZE * self.KERNEL_SIZE,  # Will cover the whole kernel
            stroke_color=WHITE,  # Matches kernel border
            fill_opacity=0,  # No fill until animation
        )

        self.add(self.shifting_square)

    def set_kernel_cell_colors(self, kernel_pos: int):
        data_col = kernel_pos % self.initial_dataset.shape[1]
        data_row = kernel_pos // self.initial_dataset.shape[1]

        min_top = max(0, data_row - 1)
        max_bottom = min(self.initial_dataset.shape[0] - 1, data_row + 1)
        min_left = max(0, data_col - 1)
        max_right = min(self.initial_dataset.shape[1] - 1, data_col + 1)

        data_cell_positions = [
            (min_top, min_left),  # Top Left
            (min_top, data_col),  # Top Middle
            (min_top, max_right),  # Top Right
            (data_row, min_left),  # Center Left
            (data_row, data_col),  # Center Middle
            (data_row, max_right),  # Center Right
            (max_bottom, min_left),  # Bottom Left
            (max_bottom, data_col),  # Bottom Middle
            (max_bottom, max_right)  # Bottom Right
        ]

        def set_cell_color(k_idx: int, d_idx: tuple[int, int]):
            data_idx = (d_idx[0] * self.data_grid.cols) + d_idx[1]

            kernel_cell = self.kernel_grid.get_cell(k_idx)
            data_cell = self.data_grid.get_cell(data_idx)

            kernel_cell.set_fill(data_cell.get_fill_color(), opacity=0)

        for k_idx, d_idx in enumerate(data_cell_positions):
            set_cell_color(k_idx, d_idx)
