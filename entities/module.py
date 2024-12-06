# entities/module.py

from entities.component import CO2Scrubber, O2Controller, PressureRegulator, HumidityController, EnvironmentalMonitor, VentilationController

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
        self.max_fe = 0.0

        # Add environmental components
        self.components = [
            CO2Scrubber(scrub_rate=5.0),
            O2Controller(desired_o2_pp=210.0),
            PressureRegulator(target_pressure=1013.0),
            HumidityController(desired_rh=50.0),
            EnvironmentalMonitor(),
            VentilationController()
        ]

    def update_components(self, dt, resources, environment):
        for comp in self.components:
            comp.update(dt, resources, environment)

    def perform_maintenance_all(self):
        for comp in self.components:
            comp.perform_maintenance()

    def repair_component(self, component_name):
        for comp in self.components:
            if comp.name == component_name:
                comp.repair()
                break

class HabitationModule(Module):
    def __init__(self):
        # Capacity of 4 beds as per previous discussions
        super().__init__("Habitation Module", capacity=4)
        # This module could have its own parameters, comfort settings, etc.
        # For now, it's just a place to assign people, possibly track comfort.
        self.beds = self.capacity  # number of beds equals capacity

    def assign_person(self, person):
        # Assign a bed if available
        if len(self.assigned_people) < self.beds:
            self.assigned_people.append(person)
            person.assigned_bed = True
            return True
        return False

    def remove_person(self, person):
        if person in self.assigned_people:
            self.assigned_people.remove(person)
            person.assigned_bed = False
