# ui.py

import pygame
from settings import GUI

class GraphicalUserInterface():
    """
    Handles UI components like displaying text.
    """
    def __init__(self):
        pygame.font.init()
        self.font_size = GUI["font_size"]
        self.font = pygame.font.SysFont(None, self.font_size)
        self.scale_text_color = GUI["scale_text_color"]

    def render_ui(self, window,game):
        self.render_scale(window)
        self.draw_simulation_time(window,game)

    def render_scale(self, window):
        """
        Renders the current zoom scale on the screen.
        """
        scale_text = self.font.render(f"Scale: {window.scale:.2f}x", True, self.scale_text_color)
        scale_position = (int(window.width*0.01),int(window.height * 0.01))
        window.display.blit(scale_text, scale_position)

    def draw_simulation_time(self, window, game):
        hours = (int(game.game_time) // 3600) % 24
        minutes = (int(game.game_time) % 3600) // 60
        time_str = f"Day {game.day_number}, Time: {hours:02d}:{minutes:02d}"
        time_surf = self.font.render(time_str, True, (255, 255, 255))
        time_position = (int(window.width*0.08),int(window.height * 0.01))
        window.display.blit(time_surf, time_position)

    def format_in_game_time(seconds):
        days = seconds // 86400
        remainder = seconds % 86400
        hours = remainder // 3600
        remainder = remainder % 3600
        minutes = remainder // 60

        if days > 0:
            return f"{days}d {hours:02d}:{minutes:02d}"
        else:
            return f"{hours:02d}:{minutes:02d}"
