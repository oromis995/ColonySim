# ui.py

import pygame
from config import RESOURCE_LABELS

def draw_top_bar(screen, base_font, resources, max_caps):
    top_bar_height = 50
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen.get_width(), top_bar_height))

    texts = []
    for res_name, res_value in resources.items():
        display_name = RESOURCE_LABELS[res_name]
        if res_name in max_caps:
            max_val = max_caps[res_name]
            text_str = f"{display_name}: {int(res_value)}/{int(max_val)}"
        else:
            text_str = f"{display_name}: {int(res_value)}"
        texts.append(text_str)

    current_size = base_font.get_height()
    min_size = 10

    def total_width_for_font_size(size):
        test_font = pygame.font.SysFont("DejaVu Sans", size)
        total_w = 20
        for txt in texts:
            text_surf = test_font.render(txt, True, (255,255,255))
            total_w += text_surf.get_width() + 50
        return total_w

    screen_w = screen.get_width()
    size = current_size
    while total_width_for_font_size(size) > screen_w and size > min_size:
        size -= 1

    font = pygame.font.SysFont("DejaVu Sans", size)
    x = 20
    y = top_bar_height // 2
    for txt in texts:
        text_surf = font.render(txt, True, (255,255,255))
        text_rect = text_surf.get_rect(midleft=(x, y))
        screen.blit(text_surf, text_rect)
        x += text_surf.get_width() + 50

def draw_simulation_time(screen, header_font, game_time, day_number):
    hours = (int(game_time) // 3600) % 24
    minutes = (int(game_time) % 3600) // 60
    time_str = f"Day {day_number}, Time: {hours:02d}:{minutes:02d}"
    time_surf = header_font.render(time_str, True, (255, 255, 255))
    screen.blit(time_surf, (20, 60))

def draw_colonist_info(screen, font, colonists):
    y_offset = 100
    for colonist in colonists:
        hunger_pct = int(colonist.hunger * 100)
        thirst_pct = int(colonist.thirst * 100)
        bathroom_pct = int(colonist.bathroom_need * 100)
        sleep_pct = int(colonist.sleep_need * 100)

        info_lines = [
            f"Name: {colonist.name}",
            f"Gender: {colonist.gender}",
            f"Age: {colonist.age}",
            f"Career: {colonist.career}",
            f"Happiness: {colonist.happiness:.2f}",
            f"Thirst: {thirst_pct}%",
            f"Bathroom Need: {bathroom_pct}%",
            f"Hunger: {hunger_pct}%",
            f"Sleep Need: {sleep_pct}%",
            f"Has Bed: {colonist.assigned_bed}",
            f"Has Job: {colonist.assigned_job}",
            f"Weight: {colonist.weight:.1f} kg",
            f"Height: {colonist.height} cm",
            f"Hair Color: {colonist.hair_color}",
            f"BMI: {colonist.bmi():.1f}",
            f"Days Without Job: {colonist.days_without_job}",
            f"Aerobic Capacity: {colonist.aerobic_capacity}",
            f"Max CO2 Tolerance: {colonist.max_co2_tolerance}",
            f"O2 Partial Pressure Range: {colonist.o2_partial_pressure_range}",
            f"Pressure Tolerance: {colonist.pressure_tolerance}",
            f"RH Preference: {colonist.rh_preference}%",
            f"Temp Preference: {colonist.temp_preference}°C"
        ]
        x_start = 20
        for line in info_lines:
            line_surf = font.render(line, True, (255, 255, 255))
            screen.blit(line_surf, (x_start, y_offset))
            y_offset += 20
