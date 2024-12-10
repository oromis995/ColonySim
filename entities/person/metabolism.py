# entities/metabolism.py

# New file: Metabolism class now dynamically computes O2 and CO2 production based on weight, gender, age, etc.
# Using NASA STD-3001 guidelines as a reference, we base daily O2 consumption and CO2 production on physiology.

from config import (TIME_SCALE, SLEEP_TIME_100, HUNGER_TIME, BATHROOM_TIME, THIRST_TIME,
                    THIRST_WEIGHT, BATHROOM_WEIGHT, HUNGER_WEIGHT, SLEEP_WEIGHT,
                    JOBLESS_PENALTY, NO_BED_PENALTY, DAILY_WEIGHT_LOSS_RATE,
                    BMI_THRESHOLD_MALE, BMI_THRESHOLD_FEMALE)

class Metabolism():
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

    def adjust_crew_resources(self, person, dt, resources):
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

    def update_crew(self, dt, crew, resources):
        # Update all crew for this tick
        for c in crew:
            self.update_person_needs(c, dt)
            self.update_happiness(c)
            self.adjust_crew_resources(c, dt, resources)

    def end_of_day_update(self, crew, resources):
        # Check for mortality due to extreme sleep deprivation
        for c in crew[:]:
            if c.sleep_need >= 3.0:
                crew.remove(c)
                resources["Population"] = max(0, resources["Population"] - 1)

        # Check for starvation/low BMI mortality
        for c in crew[:]:
            if c.hunger >= 1.0:
                c.weight = c.weight * (1.0 - DAILY_WEIGHT_LOSS_RATE)
                if self.check_mortality(c):
                    # Remove crew who died from starvation (low BMI)
                    crew.remove(c)
                    resources["Population"] = max(0, resources["Population"] - 1)
                    
    def bmi(self):
        h_m = self.height / 100.0
        return self.weight / (h_m * h_m)
    


class Metabolism():
    def __init__(self, weight_kg, height_m, age, gender, activity_level):
        """
        Initialize with basic user data.
        :param weight_kg: Weight in kilograms
        :param height_m: Height in meters
        :param age: Age in years
        :param gender: 'male' or 'female'
        :param activity_level: METs (e.g., Sedentary 1.2, Light 2.0, Moderate 3.0, Vigorous 5.0+)
        """
        self.weight_kg = weight_kg
        self.height_m = height_m
        self.age = age
        self.gender = gender.lower()
        self.activity_level = activity_level


    def resting_heart_rate(self):
        """
        Estimate resting heart rate (RHR) based on gender and age.
        :return: Resting heart rate in beats per minute.
        """
        if self.gender == 'male':
            return max(60, 70 - 0.5 * self.age)
        elif self.gender == 'female':
            return max(65, 75 - 0.5 * self.age)
        else:
            raise ValueError("Gender must be 'male' or 'female'.")

    def activity_heart_rate(self):
        """
        Calculate heart rate during activity using METs and adjusted BMI.
        Formula derived from METs and estimated VO2-to-heart rate relationship:
        HR = RHR + METs * 10 * (BMI / body_fitness_factor)
        :return: Heart rate during activity in beats per minute.
        """
        rhr = self.resting_heart_rate()
        adjusted_bmi = self.bmi()
        body_fitness_factor = 22 if self.gender == 'male' else 20  # Slightly higher for males
        heart_rate = rhr + self.activity_level * 10 * (adjusted_bmi / body_fitness_factor)
        return round(heart_rate)

    def vo2_max(self):
        """
        Estimate VO2 max using heart rate and gender.
        :return: VO2 max in mL/(kg·min).
        """
        max_hr = 220 - self.age
        rhr = self.resting_heart_rate()
        if self.gender == 'male':
            vo2_max = 15.3 * (max_hr / rhr)
        elif self.gender == 'female':
            vo2_max = 14.7 * (max_hr / rhr)
        else:
            raise ValueError("Gender must be 'male' or 'female'.")
        return vo2_max

    def activity_vo2(self):
        """
        Estimate VO2 during activity based on METs.
        :return: VO2 during activity in mL/(kg·min).
        """
        return self.activity_level * 3.5  # METs to VO2 conversion: 1 MET = 3.5 mL/(kg·min)

# Example Usage
if __name__ == "__main__":
    # User input
    weight_kg = 70  # Example weight in kilograms
    height_m = 1.75  # Example height in meters
    age = 30         # Example age
    gender = "male"  # 'male' or 'female'
    activity_level = 3.0  # Moderate activity (METs)

    # Initialize calculator
    calculator = Metabolism(weight_kg, height_m, age, gender, activity_level)

    # Outputs
    print("Adjusted BMI:", calculator.bmi())
    print("Resting Heart Rate (RHR):", calculator.resting_heart_rate(), "bpm")
    print("Heart Rate during Activity:", calculator.activity_heart_rate(), "bpm")
    print("VO2 Max:", calculator.vo2_max(), "mL/(kg·min)")
    print("VO2 during Current Activity:", calculator.activity_vo2(), "mL/(kg·min)")
