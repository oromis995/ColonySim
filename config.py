# config.py

# Comments updated: Removed static CO2 base rates.
# All metabolic rates are now dynamically computed in metabolism.py based on person attributes.

TIME_SCALE = 960

SLEEP_TIME_100 = 86400   # Time for sleep need to fully saturate if never slept
HUNGER_TIME = 43200      # Time for hunger need to fully saturate if never eaten
BATHROOM_TIME = 21600    # Time for bathroom need to fully saturate if never relieved
THIRST_TIME = 14400      # Time for thirst need to fully saturate if never drank

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

CO2_SCRUB_RATE = 5.0  # ppm per tick reduction example
