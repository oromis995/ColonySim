# entities/person.py

# Comments updated: This file now defines Person as mostly a data holder.
# Metabolic functions (happiness, O2 consumption, mortality checks) are moved to metabolism.py.

from config import BMI_THRESHOLD_MALE, BMI_THRESHOLD_FEMALE

class Person:
    def __init__(self, first_name, last_name, gender, age, career,
                 weight=70.0, height=170.0, hair_color="Brown",
                 assigned_bed=False, assigned_job=False):
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

        # Needs are now managed by metabolism.py
        self.thirst = 0.0
        self.bathroom_need = 0.0
        self.hunger = 0.0
        self.sleep_need = 0.0
        self.happiness = 1.0

        self.days_without_job = 0

        self.aerobic_capacity = 1.0
        self.max_co2_tolerance = 1000.0
        self.o2_partial_pressure_range = (140.0, 300.0)
        self.pressure_tolerance = (700.0, 1013.0)
        self.rh_preference = 50.0
        self.temp_preference = 22.0
        self.temp_adjustability = 5.0

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def bmi(self):
        # Kept as a physical attribute calculation
        h_m = self.height / 100.0
        return self.weight / (h_m * h_m)
