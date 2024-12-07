# ui.py

# This UI now uses expandable/collapsible "dropdown" sections for colonists and modules.
# Clicking on a colonist's name toggles showing their info categories.
# Clicking on an info category toggles showing detailed info for that category.
# Similarly, clicking on a module name toggles showing its components.
# Clicking on a component name toggles showing its maintenance details.
# Added a central viewfinder with colonists walking around in an isometric environment.
# Enhanced to scale based on window size and changed background color to black.

import random
import pygame
from config import RESOURCE_LABELS, TIME_SCALE

# Categories for organizing colonist info
COLONIST_INFO_CATEGORIES = {
    "Basic Info": ["Gender", "Age", "Career", "Weight", "Height", "Hair Color"],
    "Needs": ["Happiness", "Thirst", "Bathroom Need", "Hunger", "Sleep Need"],
    "Environment Preferences": ["Max CO2 Tolerance", "O2 Partial Pressure Range", "Pressure Tolerance", "RH Preference", "Temp Preference"],
    "Vitals": ["BMI", "Days Without Job", "Aerobic Capacity"]
}

# Viewfinder constants (will be scaled based on window size)
ISOMETRIC_TILE_WIDTH_RATIO = 0.05  # Ratio of window width
ISOMETRIC_TILE_HEIGHT_RATIO = 0.025  # Ratio of window height
GRID_SIZE_X = 10
GRID_SIZE_Y = 10
COLONIST_COLOR = (0, 255, 0)  # Green color for colonists
COLONIST_MOVE_SPEED_RATIO = 0.00005  # Tiles per millisecond for smooth movement

def draw_top_bar(screen, base_font, resources, max_caps, window_width, window_height):
    top_bar_height = int(window_height * 0.08)  # 8% of window height
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, window_width, top_bar_height))

    texts = []
    for res_name, res_value in resources.items():
        display_name = RESOURCE_LABELS.get(res_name, res_name)
        if res_name in max_caps:
            max_val = max_caps[res_name]
            text_str = f"{display_name}: {int(res_value)}/{int(max_val)}"
        else:
            text_str = f"{display_name}: {int(res_value)}"
        texts.append(text_str)

    # Adjust font size based on window height
    current_size = max(int(window_height * 0.02), 10)  # 2% of window height or at least 10
    min_size = 10

    def total_width_for_font_size(size):
        test_font = pygame.font.SysFont("DejaVu Sans", size)
        total_w = int(window_width * 0.025)  # Initial padding
        for txt in texts:
            text_surf = test_font.render(txt, True, (255, 255, 255))
            total_w += text_surf.get_width() + int(window_width * 0.06)  # Spacing
        return total_w

    size = current_size
    while total_width_for_font_size(size) > window_width and size > min_size:
        size -= 1

    font = pygame.font.SysFont("DejaVu Sans", size)
    x = int(window_width * 0.025)  # 2.5% of window width
    y = top_bar_height // 2
    for txt in texts:
        text_surf = font.render(txt, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midleft=(x, y))
        screen.blit(text_surf, text_rect)
        x += text_surf.get_width() + int(window_width * 0.06)  # Spacing

def draw_simulation_time(screen, header_font, game_time, day_number, window_width, window_height):
    hours = (int(game_time) // 3600) % 24
    minutes = (int(game_time) % 3600) // 60
    time_str = f"Day {day_number}, Time: {hours:02d}:{minutes:02d}"
    time_surf = header_font.render(time_str, True, (255, 255, 255))
    time_x = int(window_width * 0.025)  # 2.5% of window width
    time_y = int(window_height * 0.09)  # Positioned below top bar (8%) plus 1%
    screen.blit(time_surf, (time_x, time_y))

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

def draw_colonists_section(screen, font, colonists, ui_states, window_width, window_height):
    """
    Draw colonists as dropdowns. Clicking on a colonist's name toggles their details.
    Within a colonist's details, categories are shown as dropdowns.
    Returns a list of clickable rects and associated actions.
    """
    clickable_areas = []

    x_start = int(window_width * 0.02)  # 2% of window width
    start_y = int(window_height * 0.12)  # Start below top bar and simulation time
    line_spacing = int(window_height * 0.02)  # 2% of window height

    title_surf = font.render("Colonists:", True, (255, 255, 255))
    screen.blit(title_surf, (x_start, start_y))
    start_y += line_spacing * 2

    for colonist in colonists:
        if not getattr(colonist, 'is_alive', True):
            continue  # Skip dead colonists

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

def draw_modules_section(screen, font, modules, ui_states, window_width, window_height):
    """
    Draw modules as dropdowns. Clicking on a module toggles its components.
    Clicking on a component toggles its maintenance details.
    """
    clickable_areas = []

    x_start = int(window_width * 0.02)  # 2% of window width
    start_y = int(window_height * 0.55)  # Start lower on the screen
    line_spacing = int(window_height * 0.02)  # 2% of window height

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
            if hasattr(module, 'components') and module.components:
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
                        comp_lines = get_component_info_lines(comp, window_width, window_height)
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

def get_component_info_lines(comp, window_width, window_height):
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

def grid_to_screen(x, y, origin_x, origin_y, tile_width, tile_height):
    """
    Convert grid coordinates to isometric screen coordinates.
    """
    screen_x = (x - y) * (tile_width // 2) + origin_x
    screen_y = (x + y) * (tile_height // 2) + origin_y
    return (screen_x, screen_y)

def draw_isometric_grid(screen, origin_x, origin_y, tile_width, tile_height, grid_size_x, grid_size_y):
    """
    Draw an isometric grid.
    """
    for x in range(grid_size_x):
        for y in range(grid_size_y):
            tile_x, tile_y = grid_to_screen(x, y, origin_x, origin_y, tile_width, tile_height)
            # Define the four corners of the diamond (isometric tile)
            points = [
                (tile_x, tile_y),
                (tile_x + tile_width // 2, tile_y + tile_height // 2),
                (tile_x, tile_y + tile_height),
                (tile_x - tile_width // 2, tile_y + tile_height // 2)
            ]
            pygame.draw.polygon(screen, (169, 169, 169), points, 1)

def draw_colonist(screen, colonist, origin_x, origin_y, ui_states, game_time, tile_width, tile_height, move_speed):
    """
    Draw a colonist at their current position with smooth movement.
    """
    colonist_state = ui_states['colonist_states'].get(colonist.name, {})
    current_pos = colonist_state.get('current_position', (colonist.position[0], colonist.position[1]))
    target_pos = colonist_state.get('target_position', (colonist.position[0], colonist.position[1]))
    moving = colonist_state.get('moving', False)
    last_update_time = colonist_state.get('last_update_time', game_time)

    if not moving:
        # Choose a new target position
        possible_moves = []
        x, y = target_pos
        if x > 0:
            possible_moves.append((x - 1, y))
        if x < GRID_SIZE_X - 1:
            possible_moves.append((x + 1, y))
        if y > 0:
            possible_moves.append((x, y - 1))
        if y < GRID_SIZE_Y - 1:
            possible_moves.append((x, y + 1))
        if possible_moves:
            new_target = random.choice(possible_moves)
            colonist_state['target_position'] = new_target
            colonist_state['moving'] = True
            colonist_state['last_update_time'] = game_time
            ui_states['colonist_states'][colonist.name] = colonist_state
    else:
        # Move towards target position smoothly
        current_x, current_y = current_pos
        target_x, target_y = target_pos
        dx = target_x - current_x
        dy = target_y - current_y
        distance = (dx**2 + dy**2) ** 0.5
        if distance != 0:
            move_step = move_speed  # tiles per millisecond
            move_x = dx / distance * move_step
            move_y = dy / distance * move_step
            new_x = current_x + move_x
            new_y = current_y + move_y

            # Check if reached or passed the target
            if (dx > 0 and new_x >= target_x) or (dx < 0 and new_x <= target_x):
                new_x = target_x
            if (dy > 0 and new_y >= target_y) or (dy < 0 and new_y <= target_y):
                new_y = target_y

            colonist_state['current_position'] = (new_x, new_y)
            ui_states['colonist_states'][colonist.name] = colonist_state

            # If reached target, stop moving
            if (new_x, new_y) == target_pos:
                colonist_state['moving'] = False
                colonist_state['last_update_time'] = game_time
                ui_states['colonist_states'][colonist.name] = colonist_state

    # Convert current position to screen coordinates
    screen_x, screen_y = grid_to_screen(current_pos[0], current_pos[1], origin_x, origin_y, tile_width, tile_height)
    # Draw colonist as a circle
    pygame.draw.circle(screen, COLONIST_COLOR, (int(screen_x), int(screen_y)), max(int(tile_width * 0.2), 4))

def draw_viewfinder(screen, ui_states, game_time, colonists, window_width, window_height):
    """
    Draw the central viewfinder with the isometric environment and colonists.
    """
    # Define viewfinder position (center of the screen)
    viewfinder_width = int(window_width * 0.5)  # 50% of window width
    viewfinder_height = int(window_height * 0.8)  # 80% of window height
    viewfinder_x = (window_width - viewfinder_width) // 2
    viewfinder_y = (window_height - viewfinder_height) // 2
    viewfinder_rect = pygame.Rect(viewfinder_x, viewfinder_y, viewfinder_width, viewfinder_height)

    # Draw background for viewfinder
    pygame.draw.rect(screen, (0, 0, 0), viewfinder_rect)
    pygame.draw.rect(screen, (255, 255, 255), viewfinder_rect, 2)  # border

    # Calculate origin for isometric grid
    origin_x = viewfinder_x + viewfinder_width // 2
    origin_y = viewfinder_y + int(viewfinder_height * 0.1)  # 10% padding from top

    # Calculate tile sizes based on viewfinder size
    tile_width = int(window_width * ISOMETRIC_TILE_WIDTH_RATIO)
    tile_height = int(window_height * ISOMETRIC_TILE_HEIGHT_RATIO)

    # Draw isometric grid
    draw_isometric_grid(screen, origin_x, origin_y, tile_width, tile_height, GRID_SIZE_X, GRID_SIZE_Y)

    # Initialize colonist states if not present
    if 'colonist_states' not in ui_states:
        ui_states['colonist_states'] = {}
        for colonist in colonists:
            if not getattr(colonist, 'is_alive', True):
                continue
            ui_states['colonist_states'][colonist.name] = {
                'current_position': (colonist.position[0], colonist.position[1]),
                'target_position': (colonist.position[0], colonist.position[1]),
                'moving': False,
                'last_update_time': game_time
            }

    # Calculate movement speed based on window size
    move_speed = window_width * COLONIST_MOVE_SPEED_RATIO  # tiles per millisecond

    # Update and draw each colonist
    for colonist in colonists:
        if not getattr(colonist, 'is_alive', True):
            # Remove colonist from states if dead
            if colonist.name in ui_states['colonist_states']:
                del ui_states['colonist_states'][colonist.name]
            continue
        draw_colonist(screen, colonist, origin_x, origin_y, ui_states, game_time, tile_width, tile_height, move_speed)

    pygame.display.flip()

def draw_ui(screen, base_font, header_font, resources, max_caps, game_time, day_number, colonists, modules, ui_states):
    window_width, window_height = screen.get_size()
    screen.fill((0, 0, 0))  # Changed background color to black
    draw_top_bar(screen, base_font, resources, max_caps, window_width, window_height)
    draw_simulation_time(screen, header_font, game_time, day_number, window_width, window_height)

    clickable_areas = []
    # Draw colonists section
    colonist_areas, last_y = draw_colonists_section(screen, base_font, colonists, ui_states, window_width, window_height)
    clickable_areas.extend(colonist_areas)

    # Draw modules section below colonists
    module_areas = draw_modules_section(screen, base_font, modules, ui_states, window_width, window_height)
    clickable_areas.extend(module_areas)

    # Draw central viewfinder with colonists
    draw_viewfinder(screen, ui_states, game_time, colonists, window_width, window_height)

    return clickable_areas
