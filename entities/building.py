# entities/building.py

class Module:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.assigned_people = []

    def assign_person(self, person):
        if len(self.assigned_people) < self.capacity:
            self.assigned_people.append(person)
            return True
        return False

class CoreModule(Module):
    def __init__(self):
        super().__init__("Core Module", capacity=0)
        self.max_o2 = 3360.0
        self.max_h2o = 1000.0
        self.max_meals = 80.0
        self.max_solid_waste = 10.0
        self.max_liquid_waste = 30.0
        # Fe no building -> max Fe = 0
        self.max_fe = 0.0

class HabitationModule(Module):
    def __init__(self):
        super().__init__("Habitation Module", capacity=4)
        # Not currently used
