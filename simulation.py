# simulation.py

from config import (co2_ppm_increase_per_irl_second,
                    THIRST_INC, BATHROOM_INC, HUNGER_INC, SLEEP_INC,
                    DAILY_WEIGHT_LOSS_RATE, TIME_SCALE)
# Removed CO2_SCRUB_RATE because now in component

def update_simulation(dt, colonists, resources, max_caps, modules):
    # Construct environment from resources:
    # O2 partial pressure (o2_pp) and pressure (pressure) are hypothetical calculations.
    # We'll assume O2 partial pressure correlates with O2 level and total pressure stable.
    # Let's say total pressure stable at 1013 hPa by default, o2_pp about 210 mmHg nominal.
    # For simplicity:
    environment = {
        "CO2": resources["CO2"],
        "temp": 22.0,
        "rh": 50.0,
        "pressure": 1013.0,
        "o2_pp": 210.0
    }

    for colonist in colonists:
        colonist.thirst = min(1.0, colonist.thirst + THIRST_INC * dt)
        colonist.bathroom_need = min(1.0, colonist.bathroom_need + BATHROOM_INC * dt)
        colonist.hunger = min(1.0, colonist.hunger + HUNGER_INC * dt)
        colonist.sleep_need = min(3.0, colonist.sleep_need + SLEEP_INC * dt)
        colonist.update_happiness()

    total_co2_inc = 0.0
    for c in colonists:
        # base co2 inc
        total_co2_inc += co2_ppm_increase_per_irl_second(c.weight) * dt
    resources["CO2"] += total_co2_inc

    # Adjust O2 consumption based on colonist metabolism
    for c in colonists:
        # For now just use daily_o2_consumption fixed
        # In a real scenario, we might factor environment again
        o2_per_game_sec = c.daily_o2_consumption() / 86400.0
        o2_consumed = o2_per_game_sec * (dt * TIME_SCALE)
        resources["O2"] = max(0, resources["O2"] - o2_consumed)

    # Update Core Module components
    for m in modules:
        if m.name == "Core Module":
            m.update_components(dt, resources, environment)

    clamp_resources(resources, max_caps)

def clamp_resources(resources, max_caps):
    resources["Fe"] = max(min(resources["Fe"], 0.0), 0.0)
    for res in ["O2", "H2O", "Meals", "Solid Waste", "Liquid Waste"]:
        if res in max_caps:
            resources[res] = min(resources[res], max_caps[res])
            resources[res] = max(resources[res], 0.0)
    resources["Population"] = max(resources["Population"], 0)
    resources["CO2"] = max(resources["CO2"], 0.0)

def end_of_day_update(colonists, resources):
    for c in colonists[:]:
        if c.sleep_need >= 3.0:
            colonists.remove(c)
            resources["Population"] = max(0, resources["Population"] - 1)

    for c in colonists[:]:
        if c.hunger >= 1.0:
            c.weight = c.weight * (1.0 - DAILY_WEIGHT_LOSS_RATE)
            if c.check_mortality():
                colonists.remove(c)
                resources["Population"] = max(0, resources["Population"] - 1)
