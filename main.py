# main.py

import pygame
import sys
from grid import Grid
from gui.window import Window
from gui.gui import GraphicalUserInterface
from game import Game

def main():
    # Start the game
    game = Game()
    # Set up the display
    window = Window()
    # Initialize and draw grid
    grid = Grid()
    grid.draw_grid(window)

    # Initialize UI
    gui = GraphicalUserInterface()  

    running = True
    while running:
        dt = game.clock.tick(60) / 1000.0  # Maintain frame rate
        game.tick(dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                window.resize(event.w, event.h)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle zooming with mouse wheel
                if event.button in (4, 5):  # Mouse wheel up/down
                    # Get the mouse position
                    if event.button == 4:  # Zoom in
                        window.zoom_in(event.pos)
                    elif event.button == 5:  # Zoom out
                        window.zoom_out(event.pos)
                    
        # Handle key presses for panning using WASD
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Move left
            window.pan_left()
        if keys[pygame.K_d]:  # Move right
            window.pan_right()
        if keys[pygame.K_w]:  # Move up
            window.pan_up()
        if keys[pygame.K_s]:  # Move down
            window.pan_down()

        # Delete everything on screen
        window.clear_window()
        # Draw the rotated grid with current scale and offsets
        grid.draw_grid(window)

        gui.render_ui(window,game)
        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
