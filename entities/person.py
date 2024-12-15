# entities/person.py

import webcolors
import random
#from person import Metabolism



class Person:
    def __init__(self):
        self.health = self.generate_health()
        self.bio = self.generate_bio()
        self.needs = {"water":0.0,"bathroom":0.0,"food":0.0, "sleep":0.0, "mood":1.0}
        self.career = self.generate_career()
        self.movement = {"position":(0,0),"speed":0.5}
        self.assigned_bed = False
        self.assigned_job = False
        #self.Metabolism()
        # Needs managed by metabolism.py

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


    def generate_health(self):
        sex = random.choice(["M","F"])

        while True:
            age = random.gammavariate(2, 10) # for now implying space elves live as long as humans
            if 13 <= age <= 113:
                age = round(age)
                break
        
        height = Person.calculate_height(sex,age)
        weight = Person.calculate_weight(height)

        return {
            'age': age,
            'sex': sex,
            'weight': weight,
            'height': height  
        }

    def generate_bio(self):
        def get_random_name(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return random.choice(f.read().splitlines())
        
        gender = random.choice(["M", "F", "N"])
        first_name_file = {
            "M": "Data/assembled_m_names.txt",
            "F": "Data/assembled_f_names.txt",
            "N": "Data/assembled_n_names.txt"
        }[gender]
        
        first_name = get_random_name(first_name_file)
        last_name = get_random_name("Data/last_names.txt")
        color_name = random.choice(webcolors.names(spec='css3'))
        hair_color = {"name": color_name, "hex": webcolors.name_to_hex(color_name)}
        
        bio = {
            "first name": first_name,
            "last name": last_name,
            "gender": gender,
            "hair color": hair_color # turn it into greyer colors as the subject ages. Use HSL
        }
        return bio


    def generate_career(self):
        career = random.choice(["Physician","Mechanical Engineer","Chemical Engineer","Electrical Engineer","Aerospace Engineer","Computer Engineer","Pilot","Botanist"])
        return career


    def calculate_weight(height):

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
        return round(weight, 1)


    def calculate_height(gender,age):

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

        return round(height)
    
    
if __name__ == "__main__":
    # Generate and print 25 sample persons
    for _ in range(25):
        print("----------------------")
        person = Person()
        for b in person.bio:
            print(b,person.bio[b])
        for h in person.health:
            print(h,person.health[h])