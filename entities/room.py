# entities/room.py
from entities.room import EnvironmentalConditions

class Room():
    def __init__(self, name):
        self.name = name
        self.activities = {}
        self.environment = EnvironmentalConditions()

    def assign_person(self, person, requested_activity):
        assigned = False
        for activity in self.activities:
            #check that activity exists
            if activity == requested_activity:
                #what do if someone is already assigned? Solve later.
                self.activities[activity] = person
                assigned = True
        if assigned == False:
            # DO SOMETHING WITH THIS VISUALLY
            print("Unable to assign the activity, no activity available.")
    
    def unassign_person(self, person):
        unassigned = False
        for activity in self.activities:
            if self.activities[activity] == person:
                self.activities[activity] = ""
                unassigned = True
        if unassigned == False:
            # DO SOMETHING WITH THIS VISUALLY
            print("Unable to unassign the activity, crewman not assigned to this activity.")


class Core(Room):      

    def __init__(self, ship_resources):
        super().__init__("Core", capacity=0)
        #increase caps
        ship_resources.max_o2 =+3360.0
        ship_resources.max_h2o =+1000.0
        ship_resources.max_meals =+80.0
        ship_resources.max_solid_waste =+10.0
        ship_resources.max_liquid_waste =+30.0
        # add resources
        ship_resources.o2 = 3360.0
        ship_resources.h2o = 1000.0
        ship_resources.meals = 80.0
        ship_resources.solid_waste = 0
        ship_resources.liquid_waste = 0


        # Add environmental components    

    
        



class Quarters(Room):
    def __init__(self):
        # Capacity of 4 beds as per previous discussions
        super().__init__("Quarters", {"sleep":"","sleep":"","sleep":"","sleep":""})

    def assign_person():
        pass
        #write code here to keep beds assigned after crew member is done sleeping.
    