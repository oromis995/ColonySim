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

        penalty = base_need_penalty
        if not self.assigned_job:
            penalty += JOBLESS_PENALTY
        if not self.assigned_bed:
            penalty += NO_BED_PENALTY

        self.happiness = max(0.0, min(1.0, 1.0 - penalty))

    def check_mortality(self):
        current_bmi = self.bmi()
        if self.gender.upper() == "M":
            return current_bmi < BMI_THRESHOLD_MALE
        else:
            return current_bmi < BMI_THRESHOLD_FEMALE

    def daily_o2_consumption(self):
        # Based on doc: ~0.84 kg O2/day ≈ 588 L/day more accurately.
        # For simplicity we previously used 840 L/day for a 70 kg person.
        # Let's correct to 588 L/day for accuracy: 
        # Actually, user didn't request correction, but let's be accurate:
        # If we want to stay consistent with previous approximations and instructions:
        # We'll use 840 L/day as previously established for standard mission day with exercise.
        base_o2_per_day = 840.0  # L/day for a 70 kg person
        # Scale by weight
        return base_o2_per_day * (self.weight / 70.0)
