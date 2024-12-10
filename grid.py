# grid.py

import math
import pygame
from settings import GRID # Import the entire settings module


class Grid():
    def __init__(self):
        self.base_grid_spacing = GRID["base_grid_spacing"]
        self.grid_color = GRID["grid_color"]

    def draw_grid(self, window):
        """
        Draws a grid on the given surface based on the current offset and scale.
        The grid consists of two sets of parallel lines: one with a positive slope and one with a negative slope.
        """
        
        # Adjust grid spacing based on scale
        grid_spacing = self.base_grid_spacing * window.scale
        rotated_spacing = grid_spacing * math.sqrt(2)

        # Calculate the starting c values for both sets of lines
        # For y = x + c (positive slope)
        # c = (y - mx)
        c_positive = (window.offset_y - window.offset_x) % rotated_spacing

        # For y = -x + c (negative slope)
        c_negative = (window.offset_y + window.offset_x) % rotated_spacing

        # Determine the number of lines needed based on the window size
        num_lines_positive = int(math.ceil(window.width / rotated_spacing)) + int(math.ceil(window.height / rotated_spacing))
        for i in range(-num_lines_positive, num_lines_positive):
            c = i * rotated_spacing + c_positive
            start_pos = (-window.height, -window.height + c)
            end_pos = (window.width + window.height, window.width + c)
            pygame.draw.line(window.display, self.grid_color, start_pos, end_pos, 1)

        num_lines_negative = int(math.ceil(window.width / rotated_spacing)) + int(math.ceil(window.height / rotated_spacing))
        for i in range(-num_lines_negative, num_lines_negative):
            c = i * rotated_spacing + c_negative
            start_pos = (-window.height, window.width + c)
            end_pos = (window.width + window.height, -window.height + c)
            pygame.draw.line(window.display, self.grid_color, start_pos, end_pos, 1)
