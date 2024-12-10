# settings.py

import json
import os

# Determine the path to the settings.json file
current_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(current_dir, 'settings.json')

# Load settings from settings.json
with open(settings_path, 'r') as file:
    config = json.load(file)

# Organize settings into dictionaries
WINDOW = config.get('window', {})
GUI = config.get('gui', {})
GRID = config.get('grid', {})
TIME = config.get('time', {})
WEIGHTS = config.get('weights', {})
PENALTIES = config.get('penalties', {})
BMI = config.get('bmi', {})
INITIAL_RESOURCES = config.get('initial_resources', {})

# Example usage:
# from settings import WINDOW, TEXT, GRID, ZOOM, PANNING, TIME, NEEDS, WEIGHTS, PENALTIES, BMI, INITIAL_RESOURCES

# You can now access settings like:
# WINDOW['width'], TEXT['color'], GRID['bg_color'], etc.





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

