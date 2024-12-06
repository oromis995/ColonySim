# game.py

import sys
import pygame
from pygame.locals import QUIT, VIDEORESIZE, MOUSEBUTTONDOWN
from config import (TIME_SCALE, INITIAL_POPULATION, INITIAL_O2, INITIAL_H2O, INITIAL_MEALS,
                    INITIAL_CO2, INITIAL_SOLID_WASTE, INITIAL_LIQUID_WASTE, INITIAL_FE)
from simulation import update_simulation, end_of_day_update
from ui import draw_ui, handle_ui_click
from entities.person import Person
from entities.module import CoreModule, HabitationModule

class Game:
    def __init__(self, width=1280, height=720, title="Colony Sim"):
        pygame.init()
        
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption(title)
        
        self.clock = pygame.time.Clock()
        self.running = True

        self.modules = [
            CoreModule(),
            HabitationModule()
        ]
        core = self.modules[0]

        max_o2 = core.max_o2
        max_h2o = core.max_h2o
        max_meals = core.max_meals
        max_solid = core.max_solid_waste
        max_liquid = core.max_liquid_waste
        max_fe = 0.0

        population = INITIAL_POPULATION
        O2 = min(INITIAL_O2, max_o2)
        H2O = min(INITIAL_H2O, max_h2o)
        Meals = min(INITIAL_MEALS, max_meals)
        CO2 = INITIAL_CO2
        SolidWaste = min(INITIAL_SOLID_WASTE, max_solid)
        LiquidWaste = min(INITIAL_LIQUID_WASTE, max_liquid)
        Fe = min(INITIAL_FE, max_fe)

        self.resources = {
            "Population": population,
            "O2": O2,
            "H2O": H2O,
            "CO2": CO2,
            "Meals": Meals,
            "Solid Waste": SolidWaste,
            "Liquid Waste": LiquidWaste,
            "Fe": Fe
        }

        self.colonists = [
            Person(first_name="Alice", last_name="Smith", gender="F", age=20, career="Eng", weight=70.0, height=170.0, hair_color="Red", assigned_bed=False, assigned_job=False)
        ]

        self.simulation_time = 0.0
        self.game_time = 0.0
        self.day_number = 1

        self.base_font = pygame.font.SysFont("DejaVu Sans", 24)
        self.header_font = pygame.font.SysFont("DejaVu Sans", 36)

        self.previous_day = self.get_current_day()

        self.max_caps = {
            "O2": max_o2,
            "H2O": max_h2o,
            "Meals": max_meals,
            "Solid Waste": max_solid,
            "Liquid Waste": max_liquid
        }

        # UI states for dropdowns
        self.ui_states = {
            "colonists_expanded": {},
            "colonist_categories_expanded": {},
            "modules_expanded": {},
            "components_expanded": {}
        }

    def get_current_day(self):
        total_seconds = int(self.game_time)
        return total_seconds // 86400

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == VIDEORESIZE:
                width, height = event.size
                self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Handle UI clicks
                handled = handle_ui_click(event.pos, self.ui_states, self.clickable_areas)
                if handled:
                    # Redraw immediately after state change
                    self.draw(force_redraw=True)

    def run_simulation(self, dt):
        self.simulation_time += dt
        self.game_time += dt * TIME_SCALE
        update_simulation(dt, self.colonists, self.resources, self.max_caps, self.modules)

        current_day = self.get_current_day()
        if current_day > self.previous_day:
            self.update_jobless_days()
            end_of_day_update(self.colonists, self.resources)
            self.previous_day = current_day
            self.day_number = current_day + 1

    def update_jobless_days(self):
        for c in self.colonists:
            if not c.assigned_job:
                c.days_without_job += 1
            else:
                c.days_without_job = 0

    def draw(self, force_redraw=False):
        # draw_ui returns the clickable areas
        self.clickable_areas = draw_ui(
            self.screen, 
            self.base_font, 
            self.header_font, 
            self.resources, 
            self.max_caps, 
            self.game_time, 
            self.day_number, 
            self.colonists, 
            self.modules, 
            self.ui_states
        )

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.run_simulation(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()
