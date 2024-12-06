# entities/person.py

from config import (THIRST_WEIGHT, BATHROOM_WEIGHT, HUNGER_WEIGHT, SLEEP_WEIGHT, 
                    JOBLESS_PENALTY, NO_BED_PENALTY,
                    BMI_THRESHOLD_MALE, BMI_THRESHOLD_FEMALE)

class Person:
    def __init__(self, first_name, last_name, gender, age, career, weight=70.0, height=170.0, hair_color="Brown", assigned_bed=False, assigned_job=False):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.age = age
        self.career = career
        self.weight = weight
        self.height = height
        self.hair_color = hair_color

        self.assigned_bed = assigned_bed
        self.assigned_job = assigned_job

        self.thirst = 0.0
        self.bathroom_need = 0.0
        self.hunger = 0.0
        self.sleep_need = 0.0
        self.happiness = 1.0

        self.days_without_job = 0

        # New NASA-inspired parameters:
        # Aerobic capacity influences metabolism. Higher = more O2 needed if exercising.
        self.aerobic_capacity = 1.0  # baseline 1.0; >1.0 means higher needs

        # Tolerances and preferences (Just placeholders):
        self.max_co2_tolerance = 1000.0  # ppm, after this colonist is stressed
        self.o2_partial_pressure_range = (140.0, 300.0)  # mmHg range, just an example
        self.pressure_tolerance = (700.0, 1013.0) # total pressure in hPa, example
        self.rh_preference = 50.0  # preferred relative humidity %
        self.temp_preference = 22.0 # preferred temp in Celsius
        self.temp_adjustability = 5.0 # colonist can tolerate ±5°C from preference

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def bmi(self):
        h_m = self.height / 100.0
        return self.weight / (h_m * h_m)

    def update_happiness(self):
        thirst_val = min(self.thirst, 1.0)
        bathroom_val = min(self.bathroom_need, 1.0)
        hunger_val = min(self.hunger, 1.0)
        sleep_val = min(self.sleep_need, 1.0)

        base_need_penalty = (thirst_val * THIRST_WEIGHT) + (bathroom_val * BATHROOM_WEIGHT) + (hunger_val * HUNGER_WEIGHT) + (sleep_val * SLEEP_WEIGHT)
        if self.sleep_need > 1.0:
            extra_sleep = self.sleep_need - 1.0
            base_need_penalty += extra_sleep * SLEEP_WEIGHT * 2.0

        # Joblessness penalty scaling with days_without_job:
        if not self.assigned_job:
            jobless_scale = min(self.days_without_job / 7.0, 1.0)
            base_need_penalty += JOBLESS_PENALTY * jobless_scale

        if not self.assigned_bed:
            base_need_penalty += NO_BED_PENALTY

        # Consider environmental conditions on happiness:
        # If CO2 > max_co2_tolerance, reduce happiness more:
        # We'll do this in simulation step where we know actual environment conditions.

        self.happiness = max(0.0, min(1.0, 1.0 - base_need_penalty))

    def check_mortality(self):
        current_bmi = self.bmi()
        if self.gender.upper() == "M":
            return current_bmi < BMI_THRESHOLD_MALE
        else:
            return current_bmi < BMI_THRESHOLD_FEMALE

    def daily_o2_consumption(self):
        # More accurate O2 based on NASA doc:
        # ~0.84 kg O2/day -> 588 L/day for a 70 kg person (previous instructions)
        base_o2_per_day = 588.0
        # Scale by weight and aerobic capacity:
        return base_o2_per_day * (self.weight / 70.0) * self.aerobic_capacity

    def update_metabolism(self, environment):
        # environment dict might include: {"CO2": current_co2_ppm, "O2": current_O2_pp, "temp": celsius, "rh": relative_humidity, ...}

        # Adjust colonist's resource usage based on environment:
        co2 = environment.get("CO2", 400.0)
        temp = environment.get("temp", 22.0)
        rh = environment.get("rh", 50.0)

        # If CO2 above tolerance, colonist might be more stressed, using more O2:
        stress_factor = 1.0
        if co2 > self.max_co2_tolerance:
            stress_factor += (co2 - self.max_co2_tolerance) / 1000.0

        # If temperature is not in (temp_preference ± temp_adjustability), add stress
        if temp < (self.temp_preference - self.temp_adjustability) or temp > (self.temp_preference + self.temp_adjustability):
            stress_factor += 0.1

        # If RH different from preference by >10%, add stress
        if abs(rh - self.rh_preference) > 10:
            stress_factor += 0.1

        # stress_factor increases O2 consumption and CO2 production
        # Let's say colonist produce CO2 scaled by stress as well
        adjusted_o2_day = self.daily_o2_consumption() * stress_factor
        # We'll return adjusted daily O2, and similarly we can say CO2 production also scales with stress:
        # base_co2_day = 840 g O2/day ~ consumption. For simplicity let's just return a factor
        # The simulation can use this factor to adjust resources each tick.

        return {
            "o2_day": adjusted_o2_day,  # L/day
            "stress_factor": stress_factor
        }
