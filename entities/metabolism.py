# entities/metabolism.py

# New file: Metabolism class now dynamically computes O2 and CO2 production based on weight, gender, age, etc.
# Using NASA STD-3001 guidelines as a reference, we base daily O2 consumption and CO2 production on physiology.

from config import (TIME_SCALE, SLEEP_TIME_100, HUNGER_TIME, BATHROOM_TIME, THIRST_TIME,
                    THIRST_WEIGHT, BATHROOM_WEIGHT, HUNGER_WEIGHT, SLEEP_WEIGHT,
                    JOBLESS_PENALTY, NO_BED_PENALTY, DAILY_WEIGHT_LOSS_RATE,
                    BMI_THRESHOLD_MALE, BMI_THRESHOLD_FEMALE)

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

    def daily_o2_consumption(self, person):
        # Base: ~0.84 kg O2/day for a reference adult (NASA), ~588 L O2/day.
        # Adjust by weight (linear), gender (males slightly higher), and aerobic capacity.
        # For simplicity: Males +5% O2 need, females base 1.0.
        # Could also factor age in if desired. For now, we skip age complexity.

        gender_factor = 1.05 if person.gender.upper() == "M" else 1.0
        weight_factor = person.weight / 70.0
        # Daily O2 in L/day:
        daily_o2 = 588.0 * weight_factor * gender_factor * person.aerobic_capacity
        return daily_o2

    def daily_co2_production(self, person):
        # According to NASA references, CO2 production roughly correlates with O2 consumption.
        # Typical respiratory quotient ~0.85, meaning CO2 produced is about 85% of O2 volume consumed.
        # So if daily O2 ~ 588 L/day, CO2 ~ 588 * 0.85 = ~500 L/day.
        # We'll dynamically compute based on their adjusted O2 consumption:
        daily_o2 = self.daily_o2_consumption(person)
        RQ = 0.85
        return daily_o2 * RQ  # L CO2/day

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
        # O2 consumption:
        daily_o2 = self.daily_o2_consumption(person)
        o2_per_day = daily_o2  # L/day
        o2_per_game_sec = o2_per_day / 86400.0
        o2_consumed = o2_per_game_sec * (dt * TIME_SCALE)
        resources["O2"] = max(0, resources["O2"] - o2_consumed)

        # CO2 production:
        daily_co2 = self.daily_co2_production(person)
        co2_per_day = daily_co2  # L/day equivalent
        # Convert CO2 volume to ppm increment: 
        # Previously, CO2 was tracked as ppm directly. For simplicity, we can assume a linear environment volume.
        # Let's say 1 ppm increment = 1 L in some reference volume. This is a gross simplification.
        # Without a defined habitat volume, we just treat this "CO2" resource as ppm units.
        # We'll scale similarly to how O2 is consumed. For now, let's keep increment directly as if CO2 resource is ppm storage.
        co2_per_game_sec = co2_per_day / 86400.0
        co2_produced = co2_per_game_sec * (dt * TIME_SCALE)
        resources["CO2"] += co2_produced

    def update_colonists(self, dt, colonists, resources):
        # Update all colonists for this tick
        for c in colonists:
            self.update_person_needs(c, dt)
            self.update_happiness(c)
            self.adjust_colonist_resources(c, dt, resources)

    def end_of_day_update(self, colonists, resources):
        # Check for mortality due to extreme sleep deprivation
        for c in colonists[:]:
            if c.sleep_need >= 3.0:
                colonists.remove(c)
                resources["Population"] = max(0, resources["Population"] - 1)

        # Check for starvation/low BMI mortality
        for c in colonists[:]:
            if c.hunger >= 1.0:
                c.weight = c.weight * (1.0 - DAILY_WEIGHT_LOSS_RATE)
                if self.check_mortality(c):
                    # Remove colonist who died from starvation (low BMI)
                    colonists.remove(c)
                    resources["Population"] = max(0, resources["Population"] - 1)
