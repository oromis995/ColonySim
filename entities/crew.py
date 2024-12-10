from entities.person import Person

class Crew():
    
    def __init__(self):
        first_colonist = Person(first_name="Alice", last_name="Laine", gender="F", age=20, career="Eng", weight=70.0, height=170.0, hair_color="Red", assigned_bed=False, assigned_job=False)
        self.crew = [first_colonist]
   