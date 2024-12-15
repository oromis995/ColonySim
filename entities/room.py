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

    def __init__(self, ship):
        super().__init__("Core")

        ship.resources = {"o2":ship.resources["o2"]+3360.0,
                          "h2o":ship.resources["h2o"]+1000.0,
                          "canned_food":ship.resources["canned_food"]+80,
                          "solid_waste":0,
                          "liquid_waste":0}
        ship.resource_caps = {"o2":ship.resource_caps["o2"]+3360.0,
                          "h2o":ship.resource_caps["h2o"]+1000.0,
                          "canned_food":ship.resource_caps["canned_food"]+80,
                          "solid_waste":ship.resource_caps["solid_waste"]+10,
                          "liquid_waste":ship.resource_caps["liquid_waste"]+30}

        # Add environmental components    

class Quarters(Room):
    def __init__(self):
        # Capacity of 4 beds as per previous discussions
        super().__init__("Quarters")
        self.activities = {"sleep":"","sleep":"","sleep":"","sleep":""}

    def assign_person():
        pass
        #write code here to keep beds assigned after crew member is done sleeping.
    