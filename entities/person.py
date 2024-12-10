# entities/person.py
from pynames import GENDER
from pynames.generators.elven import DnDNamesGenerator
from person import Metabolism

import random

class Person:
    def __init__(self, bio, health, career, needs, position):
        self.bio = bio
        self.health = health
        self.needs = needs
        self.career = career
        self.position = position
        self.assigned_bed = False
        self.assigned_job = False
        self.Metabolism()
        # Needs managed by metabolism.py
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


    def generate_health():
        gender = random.choice(["M","F"])

        while True:
            age = random.gammavariate(2, 10) # for now implying space elves live as long as humans
            if 13 <= age <= 113:
                age = round(age)
                break
        female_teen_height = [156.4,159.8,161.7,162.5,162.9,163.1,163.2]
        male_teen_height = [156.0,163.2,169.0,172.9,175.2,176.1,176.5]
        # Generate height based on age and gender
        if age < 19:
            # Simple linear growth model until age 18
            if gender == 'M':
                # Assume height at age 13 is 140 cm and grows ~6 cm per year
                mean_height = male_teen_height[age-13]
            else:
                # Assume height at age 13 is 135 cm and grows ~5.5 cm per year
                mean_height = female_teen_height[age-13]
            height = random.gauss(mean_height, 5)  # Reduced std dev for children
        else:
            # Adult height distribution
            if gender == 'M':
                mean_height = 178.4  # Average adult male height in cm
                height = random.gauss(mean_height, 7.59)
            else:
                mean_height = 164.7  # Average adult female height in cm
                height = random.gauss(mean_height, 7.07)
            
        
        height = round(height)

        # Calculate mean weight based on BMI = 22
        height_m = height / 100  # Convert height to meters
        mean_weight = 22 * (height_m ** 2)  # BMI formula rearranged

        # Set variance as 10% of the mean squared for realistic variability
        variance = (0.1 * mean_weight) ** 2

        # Calculate gamma distribution parameters
        shape = (mean_weight ** 2) / variance
        scale = variance / mean_weight

        # Generate weight using gamma distribution
        weight = random.gammavariate(shape, scale)
        weight = round(weight, 1)

        return {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height  
        }
    
    def make_random_person(self):
        
        career = random.choice(["Physician","Mechanical Engineer","Chemical Engineer","Electrical Engineer","Aerospace Engineer","Computer Engineer","Pilot","Botanist"])
        health = self.generate_health()
        elven_generator = DnDNamesGenerator()
        position=0,0
        bio = {"first name":elven_generator.get_name_simple(GENDER.MALE if health["gender"]=="M" else GENDER.FEMALE),
               "last name":elven_generator.get_name_simple(GENDER.MALE if health["gender"]=="M" else GENDER.FEMALE),
               "hair color": ""}
        needs = {"water":0.0,"bathroom":0.0,"food":0.0, "sleep":0.0, "mood":1.0}
        person = Person(bio,health,career,needs,position)
        return person

    
if __name__ == "__main__":
    # Generate and print 5 sample persons
    for _ in range(25):
        person = Person.generate_health()
        print(person)