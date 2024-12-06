# config.py

TIME_SCALE = 960

SLEEP_TIME_100 = 86400
HUNGER_TIME = 43200
BATHROOM_TIME = 21600
THIRST_TIME = 14400

def need_increment_per_irl_sec(in_game_time_for_100):
    return (1.0 / in_game_time_for_100) * TIME_SCALE

THIRST_INC = need_increment_per_irl_sec(THIRST_TIME)
BATHROOM_INC = need_increment_per_irl_sec(BATHROOM_TIME)
HUNGER_INC = need_increment_per_irl_sec(HUNGER_TIME)
SLEEP_INC = need_increment_per_irl_sec(SLEEP_TIME_100)

BASE_CO2_PER_GAME_SEC = 0.0003
CO2_BASE_RATE_IRL = BASE_CO2_PER_GAME_SEC * TIME_SCALE

def co2_ppm_increase_per_irl_second(weight):
    return (weight / 70.0) * CO2_BASE_RATE_IRL

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

# Initial conditions
INITIAL_POPULATION = 1
INITIAL_O2 = 4000.0
INITIAL_H2O = 1200.0
INITIAL_MEALS = 100.0
INITIAL_CO2 = 400.0
INITIAL_SOLID_WASTE = 0.0
INITIAL_LIQUID_WASTE = 0.0
INITIAL_FE = 0.0  # Now Fe = 0 initially.
