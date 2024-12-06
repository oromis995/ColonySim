# simulation.py
from config import (co2_ppm_increase_per_irl_second,
                    THIRST_INC, BATHROOM_INC, HUNGER_INC, SLEEP_INC,
                    DAILY_WEIGHT_LOSS_RATE, TIME_SCALE)

def update_simulation(dt, colonists, resources, max_caps):
    # Update needs
    for colonist in colonists:
        colonist.thirst = min(1.0, colonist.thirst + THIRST_INC * dt)
        colonist.bathroom_need = min(1.0, colonist.bathroom_need + BATHROOM_INC * dt)
        colonist.hunger = min(1.0, colonist.hunger + HUNGER_INC * dt)
        colonist.sleep_need = min(3.0, colonist.sleep_need + SLEEP_INC * dt)
        colonist.update_happiness()

    # CO2 increase
    total_co2_inc = 0.0
    for c in colonists:
        total_co2_inc += co2_ppm_increase_per_irl_second(c.weight) * dt
    resources["CO2"] += total_co2_inc

    # O2 consumption
    # O2 per day per colonist
    # O2 consumption per game second = colonist.daily_o2_consumption() / 86400
    for c in colonists:
        o2_per_game_sec = c.daily_o2_consumption() / 86400.0
        # dt * TIME_SCALE = game seconds elapsed
        o2_consumed = o2_per_game_sec * (dt * TIME_SCALE)
        resources["O2"] = max(0, resources["O2"] - o2_consumed)

    # After all changes, clamp resources to their caps
    clamp_resources(resources, max_caps)

def clamp_resources(resources, max_caps):
    # Population, CO2, and Fe have special conditions:
    # Fe max is 0
    resources["Fe"] = min(resources["Fe"], 0.0)  # can't go above 0
    resources["Fe"] = max(resources["Fe"], 0.0)  # also can't go below 0

    # Other resources:
    for res in ["O2", "H2O", "Meals", "Solid Waste", "Liquid Waste"]:
        if res in max_caps:
            resources[res] = min(resources[res], max_caps[res])
            resources[res] = max(resources[res], 0.0)
    # Population, CO2 no max given, just ensure not below 0
    resources["Population"] = max(resources["Population"], 0)
    resources["CO2"] = max(resources["CO2"], 0.0)

def end_of_day_update(colonists, resources):
    # Mortality checks here:
    # Sleep death
    for c in colonists[:]:
        if c.sleep_need >= 3.0:
            colonists.remove(c)
            resources["Population"] = max(0, resources["Population"] - 1)

    # Hunger -> weight loss -> BMI death
    for c in colonists[:]:
        if c.hunger >= 1.0:
            c.weight = c.weight * (1.0 - DAILY_WEIGHT_LOSS_RATE)
            if c.check_mortality():
                colonists.remove(c)
                resources["Population"] = max(0, resources["Population"] - 1)
