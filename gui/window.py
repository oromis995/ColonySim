# WINDOW["py

import pygame
from settings import WINDOW


class Window():
    def __init__(self):
        self.offset_x, self.offset_y = 0, 0
        self.width, self.height = WINDOW["width"], WINDOW["height"]
        self.bg_color = WINDOW["bg_color"]
        self.pan_speed = WINDOW["pan_speed"]
        self.min_scale = WINDOW["min_scale"]
        self.max_scale = WINDOW["max_scale"]
        self.zoom_step = WINDOW["zoom_step"]
        self.caption = WINDOW["caption"]
        self.scale = 1
        self.display = pygame.display.set_mode((self.width,self.height), pygame.RESIZABLE)
        self.clear_window()
        pygame.display.set_caption(self.caption)
        
    
    def resize(self,new_width,new_height):
        self.width, self.height = (new_width,new_height)
        self.display = pygame.display.set_mode((self.width,self.height), pygame.RESIZABLE)

    def zoom_in(self,mouse_pos):
        # Calculate the world coordinates before scaling
        world_x_before = (mouse_pos[0] - self.offset_x) / self.scale
        world_y_before = (mouse_pos[1] - self.offset_y) / self.scale
        # Adjust scale
        new_scale = self.scale + self.zoom_step
        if new_scale > self.max_scale:
            new_scale = self.max_scale
        # Calculate the new offsets to keep the world point under the mouse stationary
        self.offset_x = mouse_pos[0] - world_x_before * new_scale
        self.offset_y = mouse_pos[1] - world_y_before * new_scale
        # Update the scale
        self.scale = new_scale
    
    def zoom_out(self,mouse_pos):
        # Calculate the world coordinates before scaling
        world_x_before = (mouse_pos[0] - self.offset_x) / self.scale
        world_y_before = (mouse_pos[1] - self.offset_y) / self.scale
        # Adjust scale
        new_scale = self.scale - self.zoom_step
        if new_scale < self.min_scale:
            new_scale = self.min_scale
        # Calculate the new offsets to keep the world point under the mouse stationary
        self.offset_x = mouse_pos[0] - world_x_before * new_scale
        self.offset_y = mouse_pos[1] - world_y_before * new_scale
        # Update the scale
        self.scale = new_scale

    def pan_left(self):
        self.offset_x += self.pan_speed
    
    def pan_right(self):
        self.offset_x -= self.pan_speed

    def pan_down(self):
        self.offset_y -= self.pan_speed

    def pan_up(self):
        self.offset_y += self.pan_speed

    def clear_window(self):
        self.display.fill((self.bg_color[0],self.bg_color[1],self.bg_color[2]))