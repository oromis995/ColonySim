# config.py

# Comments updated: This file now only contains constants and resource labels.
# All metabolic calculation functions have been moved to metabolism.py.

TIME_SCALE = 960

SLEEP_TIME_100 = 86400
HUNGER_TIME = 43200
BATHROOM_TIME = 21600
THIRST_TIME = 14400

BASE_CO2_PER_GAME_SEC = 0.0003
CO2_BASE_RATE_IRL = BASE_CO2_PER_GAME_SEC * TIME_SCALE

RESOURCE_LABELS = {
    "Population": "Population",
    "O2": "O₂ (L)",
    "H2O": "H₂O (L)",
    "CO2": "CO₂ (ppm)",
    "Meals": "Meals",
    "Solid Waste": "Solid Waste (L)",
    "Liquid Waste": "Liquid Waste (L)",
    "Fe": "Fe"
}

THIRST_WEIGHT = 0.4
BATHROOM_WEIGHT = 0.3
HUNGER_WEIGHT = 0.2
SLEEP_WEIGHT = 0.3
JOBLESS_PENALTY = 0.05
NO_BED_PENALTY = 0.1

BMI_THRESHOLD_MALE = 13.0
BMI_THRESHOLD_FEMALE = 11.0
DAILY_WEIGHT_LOSS_RATE = 0.005

INITIAL_POPULATION = 1
INITIAL_O2 = 4000.0
INITIAL_H2O = 1200.0
INITIAL_MEALS = 100.0
INITIAL_CO2 = 400.0
INITIAL_SOLID_WASTE = 0.0
INITIAL_LIQUID_WASTE = 0.0
INITIAL_FE = 0.0

CO2_SCRUB_RATE = 5.0  # ppm per tick reduction example rate
