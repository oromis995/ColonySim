import room

class Ship():
    
    def __init__(self):
        self.base_resources = {"o2":0,"h2o":0,"meals":0,"solid_waste":0,"liquid_waste":0}
        self.base_caps = {"o2":0,"h2o":0,"meals":0,"solid_waste":0,"liquid_waste":0}
        #add random rooms with random number generator once more rooms are added
        self.rooms = [room.Core()]
        self.crew = []
