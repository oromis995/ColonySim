from settings import TIME
import pygame

class Game:
    def __init__(self):
        self.time_scale = TIME["time_scale"]
        self.time = 0.0
        self.game_time = 0.0
        self.day_number = 1
        self.previous_day = self.get_current_day()
        self.clock = pygame.time.Clock()
        self.running = True
        # Initialize Pygame
        pygame.init()

    def get_current_day(self):
        total_seconds = int(self.game_time)
        return total_seconds // 86400

    def tick(self, dt):
        self.time += dt
        self.game_time += dt * self.time_scale
        update_simulation(dt)
        current_day = self.get_current_day()
        if current_day > self.previous_day:
            end_of_day_update()
            self.previous_day = current_day
            self.day_number = current_day + 1


def update_simulation(dt):

    # Update crew via dynamic metabolism
    # metab.update_crew(dt, crew, resource_object)
    # Update state of ship components and rooms
    pass
    #clamp_resources(resource_object)

"""
def clamp_resources(resource_object):
    resources = resource_object.base_resources
    caps = resource_object.base_caps
    for res in resources:
        if res in caps:
            resources[res] = max(0.0, min(resources[res], caps[res]))
"""

def end_of_day_update():
    # Delegate end-of-day logic to Metabolism
    # metab.end_of_day_update(crew, resources)
    pass
    