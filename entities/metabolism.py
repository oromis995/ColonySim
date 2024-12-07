# entities/metabolism.py

# New file: This class consolidates all metabolic functions previously spread across config, person, and simulation.
# It handles increments of thirst/hunger/sleep/bathroom, O2 consumption, CO2 production, happiness, and mortality checks.

from config import (TIME_SCALE, SLEEP_TIME_100, HUNGER_TIME, BATHROOM_TIME, THIRST_TIME,
                    THIRST_WEIGHT, BATHROOM_WEIGHT, HUNGER_WEIGHT, SLEEP_WEIGHT,
                    JOBLESS_PENALTY, NO_BED_PENALTY, DAILY_WEIGHT_LOSS_RATE,
                    BMI_THRESHOLD_MALE, BMI_THRESHOLD_FEMALE, CO2_BASE_RATE_IRL)

class Metabolism:
    def __init__(self):
        # Precompute increments per IRL second
        self.thirst_inc = self.need_increment_per_irl_sec(THIRST_TIME)
        self.bathroom_inc = self.need_increment_per_irl_sec(BATHROOM_TIME)
        self.hunger_inc = self.need_increment_per_irl_sec(HUNGER_TIME)
        self.sleep_inc = self.need_increment_per_irl_sec(SLEEP_TIME_100)

    def need_increment_per_irl_sec(self, in_game_time_for_100):
        # Calculate how fast a need increases per real second
        return (1.0 / in_game_time_for_100) * TIME_SCALE

    def co2_ppm_increase_per_irl_second(self, weight):
        # Calculate CO2 production rate based on weight
        # Previously in config, moved here for metabolic consolidation
        return (weight / 70.0) * CO2_BASE_RATE_IRL

    def daily_o2_consumption(self, person):
        # Moved from Person: returns daily O2 consumption in L/day
        base_o2_per_day = 588.0
        return base_o2_per_day * (person.weight / 70.0) * person.aerobic_capacity

    def update_person_needs(self, person, dt):
        # Increment metabolic needs over dt seconds
        person.thirst = min(1.0, person.thirst + self.thirst_inc * dt)
        person.bathroom_need = min(1.0, person.bathroom_need + self.bathroom_inc * dt)
        person.hunger = min(1.0, person.hunger + self.hunger_inc * dt)
        person.sleep_need = min(3.0, person.sleep_need + self.sleep_inc * dt)

    def update_happiness(self, person):
        # Calculate happiness based on needs and conditions
        thirst_val = min(person.thirst, 1.0)
        bathroom_val = min(person.bathroom_need, 1.0)
        hunger_val = min(person.hunger, 1.0)
        sleep_val = min(person.sleep_need, 1.0)

        base_need_penalty = (thirst_val * THIRST_WEIGHT) + \
                            (bathroom_val * BATHROOM_WEIGHT) + \
                            (hunger_val * HUNGER_WEIGHT) + \
                            (sleep_val * SLEEP_WEIGHT)

        if person.sleep_need > 1.0:
            extra_sleep = person.sleep_need - 1.0
            base_need_penalty += extra_sleep * SLEEP_WEIGHT * 2.0

        if not person.assigned_job:
            jobless_scale = min(person.days_without_job / 7.0, 1.0)
            base_need_penalty += JOBLESS_PENALTY * jobless_scale

        if not person.assigned_bed:
            base_need_penalty += NO_BED_PENALTY

        # Clamp happiness
        person.happiness = max(0.0, min(1.0, 1.0 - base_need_penalty))

    def check_mortality(self, person):
        # Check if person dies due to low BMI
        current_bmi = person.bmi()
        if person.gender.upper() == "M":
            return current_bmi < BMI_THRESHOLD_MALE
        else:
            return current_bmi < BMI_THRESHOLD_FEMALE

    def adjust_colonist_resources(self, person, dt, resources):
        # Adjust resources based on colonist metabolism
        # O2 consumption per second:
        o2_per_day = self.daily_o2_consumption(person)
        o2_per_game_sec = o2_per_day / 86400.0
        o2_consumed = o2_per_game_sec * (dt * TIME_SCALE)
        resources["O2"] = max(0, resources["O2"] - o2_consumed)

        # CO2 production:
        total_co2_inc = self.co2_ppm_increase_per_irl_second(person.weight) * dt
        resources["CO2"] += total_co2_inc

    def update_colonists(self, dt, colonists, resources):
        # Update all colonists for this tick
        for c in colonists:
            self.update_person_needs(c, dt)
            self.update_happiness(c)
            self.adjust_colonist_resources(c, dt, resources)

    def end_of_day_update(self, colonists, resources):
        # End of day hunger/mortality check
        for c in colonists[:]:
            if c.sleep_need >= 3.0:
                # Remove colonist who is sleep deprived beyond limit
                colonists.remove(c)
                resources["Population"] = max(0, resources["Population"] - 1)

        for c in colonists[:]:
            if c.hunger >= 1.0:
                c.weight = c.weight * (1.0 - DAILY_WEIGHT_LOSS_RATE)
                if self.check_mortality(c):
                    # Remove colonist who died from starvation (low BMI)
                    colonists.remove(c)
                    resources["Population"] = max(0, resources["Population"] - 1)
