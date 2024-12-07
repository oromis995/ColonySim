# ui.py

# This UI now uses expandable/collapsible "dropdown" sections for colonists and modules.
# Clicking on a colonist's name toggles showing their info categories.
# Clicking on an info category toggles showing detailed info for that category.
# Similarly, clicking on a module name toggles showing its components.
# Clicking on a component name toggles showing its maintenance details.

import pygame
from config import RESOURCE_LABELS, TIME_SCALE

# Categories for organizing colonist info
COLONIST_INFO_CATEGORIES = {
    "Basic Info": ["Gender", "Age", "Career", "Weight", "Height", "Hair Color"],
    "Needs": ["Happiness", "Thirst", "Bathroom Need", "Hunger", "Sleep Need"],
    "Environment Preferences": ["Max CO2 Tolerance", "O2 Partial Pressure Range", "Pressure Tolerance", "RH Preference", "Temp Preference"],
    "Vitals": ["BMI", "Days Without Job", "Aerobic Capacity"]
}

def draw_top_bar(screen, base_font, resources, max_caps):
    top_bar_height = 50
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen.get_width(), top_bar_height))

    texts = []
    for res_name, res_value in resources.items():
        display_name = RESOURCE_LABELS.get(res_name, res_name)
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

def draw_colonists_section(screen, font, colonists, ui_states, x_start=20, start_y=100, line_spacing=20):
    """
    Draw colonists as dropdowns. Clicking on a colonist's name toggles their details.
    Within a colonist's details, categories are shown as dropdowns.
    Returns a list of clickable rects and associated actions.
    """
    clickable_areas = []

    title_surf = font.render("Colonists:", True, (255, 255, 255))
    screen.blit(title_surf, (x_start, start_y))
    start_y += line_spacing * 2

    for colonist in colonists:
        c_name = f"{colonist.name}"
        color = (255, 255, 0)
        # Indicate expanded or collapsed
        prefix = "-" if ui_states["colonists_expanded"].get(colonist.name, False) else "+"
        name_line = f"{prefix} {c_name}"
        name_surf = font.render(name_line, True, color)
        name_rect = name_surf.get_rect(topleft=(x_start, start_y))
        screen.blit(name_surf, name_rect)
        clickable_areas.append(("toggle_colonist", colonist.name, name_rect))
        start_y += line_spacing

        if ui_states["colonists_expanded"].get(colonist.name, False):
            # Show categories
            for cat_name, fields in COLONIST_INFO_CATEGORIES.items():
                cat_prefix = "-" if ui_states["colonist_categories_expanded"].get(colonist.name, {}).get(cat_name, False) else "+"
                cat_line = f"   {cat_prefix} {cat_name}"
                cat_surf = font.render(cat_line, True, (200, 200, 200))
                cat_rect = cat_surf.get_rect(topleft=(x_start, start_y))
                screen.blit(cat_surf, cat_rect)
                clickable_areas.append(("toggle_colonist_category", (colonist.name, cat_name), cat_rect))
                start_y += line_spacing

                if ui_states["colonist_categories_expanded"].get(colonist.name, {}).get(cat_name, False):
                    # Display info fields under this category
                    info_lines = get_colonist_info_lines(colonist)
                    # info_lines is a dict of {field_name: value}, we'll display the ones in this category
                    for f in fields:
                        val = info_lines.get(f, "")
                        info_str = f"       {f}: {val}"
                        info_surf = font.render(info_str, True, (220, 220, 220))
                        screen.blit(info_surf, (x_start, start_y))
                        start_y += line_spacing
            start_y += line_spacing

    return clickable_areas, start_y

def get_colonist_info_lines(colonist):
    # Flatten colonist info into a dict
    hunger_pct = int(colonist.hunger * 100)
    thirst_pct = int(colonist.thirst * 100)
    bathroom_pct = int(colonist.bathroom_need * 100)
    sleep_pct = int(colonist.sleep_need * 100)
    
    info = {
        "Name": colonist.name,
        "Gender": colonist.gender,
        "Age": colonist.age,
        "Career": colonist.career,
        "Happiness": f"{colonist.happiness:.2f}",
        "Thirst": f"{thirst_pct}%",
        "Bathroom Need": f"{bathroom_pct}%",
        "Hunger": f"{hunger_pct}%",
        "Sleep Need": f"{sleep_pct}%",
        "Has Bed": colonist.assigned_bed,
        "Has Job": colonist.assigned_job,
        "Weight": f"{colonist.weight:.1f} kg",
        "Height": f"{colonist.height} cm",
        "Hair Color": colonist.hair_color,
        "BMI": f"{colonist.bmi():.1f}",
        "Days Without Job": colonist.days_without_job,
        "Aerobic Capacity": colonist.aerobic_capacity,
        "Max CO2 Tolerance": colonist.max_co2_tolerance,
        "O2 Partial Pressure Range": colonist.o2_partial_pressure_range,
        "Pressure Tolerance": colonist.pressure_tolerance,
        "RH Preference": f"{colonist.rh_preference}%",
        "Temp Preference": f"{colonist.temp_preference}°C"
    }
    return info

def draw_modules_section(screen, font, modules, ui_states, x_start=20, start_y=0, line_spacing=20):
    """
    Draw modules as dropdowns. Clicking on a module toggles its components.
    Clicking on a component toggles its maintenance details.
    """
    clickable_areas = []

    title_surf = font.render("Modules:", True, (255, 255, 255))
    screen.blit(title_surf, (x_start, start_y))
    start_y += line_spacing * 2

    for module in modules:
        prefix = "-" if ui_states["modules_expanded"].get(module.name, False) else "+"
        mod_line = f"{prefix} {module.name} (Capacity: {module.capacity})"
        mod_surf = font.render(mod_line, True, (255, 255, 0))
        mod_rect = mod_surf.get_rect(topleft=(x_start, start_y))
        screen.blit(mod_surf, mod_rect)
        clickable_areas.append(("toggle_module", module.name, mod_rect))
        start_y += line_spacing

        if ui_states["modules_expanded"].get(module.name, False):
            # Show components if any
            if hasattr(module, 'components'):
                for comp in module.components:
                    comp_prefix = "-" if ui_states["components_expanded"].get((module.name, comp.name), False) else "+"
                    comp_line = f"   {comp_prefix} {comp.name}"
                    comp_surf = font.render(comp_line, True, (200, 200, 200))
                    comp_rect = comp_surf.get_rect(topleft=(x_start, start_y))
                    screen.blit(comp_surf, comp_rect)
                    clickable_areas.append(("toggle_component", (module.name, comp.name), comp_rect))
                    start_y += line_spacing

                    if ui_states["components_expanded"].get((module.name, comp.name), False):
                        # Show component details
                        comp_lines = get_component_info_lines(comp)
                        for cl in comp_lines:
                            cl_surf = font.render("       " + cl, True, (220, 220, 220))
                            screen.blit(cl_surf, (x_start, start_y))
                            start_y += line_spacing
                start_y += line_spacing
            else:
                no_comp_surf = font.render("   No components in this module.", True, (200, 200, 200))
                screen.blit(no_comp_surf, (x_start, start_y))
                start_y += line_spacing

    return clickable_areas

def get_component_info_lines(comp):
    in_game_maintenance_time = int(comp.time_since_maintenance * TIME_SCALE)
    formatted_maint_time = format_in_game_time(in_game_maintenance_time)
    comp_interval_in_game = int(comp.maintenance_interval * TIME_SCALE)
    formatted_interval = format_in_game_time(comp_interval_in_game)
    lines = [
        f"Operational: {comp.operational}",
        f"Condition: {comp.condition:.2f}",
        f"Time Since Maintenance: {formatted_maint_time}",
        f"Maintenance Interval: {formatted_interval}"
    ]
    return lines

def handle_ui_click(pos, ui_states, clickable_areas):
    # Check if pos is within any clickable rect
    # If so, perform the associated action
    x, y = pos
    for (action, target, rect) in clickable_areas:
        if rect.collidepoint(x, y):
            if action == "toggle_colonist":
                name = target
                expanded = ui_states["colonists_expanded"].get(name, False)
                ui_states["colonists_expanded"][name] = not expanded
            elif action == "toggle_colonist_category":
                c_name, cat_name = target
                if c_name not in ui_states["colonist_categories_expanded"]:
                    ui_states["colonist_categories_expanded"][c_name] = {}
                expanded = ui_states["colonist_categories_expanded"][c_name].get(cat_name, False)
                ui_states["colonist_categories_expanded"][c_name][cat_name] = not expanded
            elif action == "toggle_module":
                m_name = target
                expanded = ui_states["modules_expanded"].get(m_name, False)
                ui_states["modules_expanded"][m_name] = not expanded
            elif action == "toggle_component":
                (m_name, c_name) = target
                expanded = ui_states["components_expanded"].get((m_name, c_name), False)
                ui_states["components_expanded"][(m_name, c_name)] = not expanded
            return True
    return False

def draw_ui(screen, base_font, header_font, resources, max_caps, game_time, day_number, colonists, modules, ui_states):
    screen.fill((34, 139, 34))
    draw_top_bar(screen, base_font, resources, max_caps)
    draw_simulation_time(screen, header_font, game_time, day_number)

    clickable_areas = []
    # Draw colonists section
    colonist_areas, last_y = draw_colonists_section(screen, base_font, colonists, ui_states, start_y=100)
    clickable_areas.extend(colonist_areas)

    # Draw modules section below colonists
    module_areas = draw_modules_section(screen, base_font, modules, ui_states, start_y=last_y+40)
    clickable_areas.extend(module_areas)

    pygame.display.flip()
    return clickable_areas
