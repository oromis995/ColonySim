
class Item:
    def __init__(self, name):
        self.name = name

class ReplacementPart(Item):
    def __init__(self, name, wear_limit):
        super().__init__(name)
        self.wear = 0
        self.wear_limit = wear_limit
        self.is_operational = True

    def apply_wear(self, amount):
        self.wear += amount
        if self.wear >= self.wear_limit:
            self.is_operational = False
