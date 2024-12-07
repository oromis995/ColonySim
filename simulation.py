# simulation.py

# Comments updated: Metabolic logic (increments, O2/CO2 calculations, end_of_day_update) moved to metabolism.py.
# This file now just sets up environment and delegates metabolic updates to Metabolism.

from config import TIME_SCALE
from entities.metabolism import Metabolism

metab = Metabolism()

def update_simulation(dt, colonists, resources, max_caps, modules):
    # Construct environment (for future environmental-based metabolism if needed)
    environment = {
        "CO2": resources["CO2"],
        "temp": 22.0,
        "rh": 50.0,
        "pressure": 1013.0,
        "o2_pp": 210.0
    }

    # Now rely on Metabolism class for colonist updates
    metab.update_colonists(dt, colonists, resources)

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
    # Delegate end-of-day logic to Metabolism
    metab.end_of_day_update(colonists, resources)
