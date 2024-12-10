# entities/components.py



class Component:
    def __init__(self, name):
        self.name = name
        self.operational = True
        self.condition = 1.0  # 1.0 = perfect condition, 0.0 = broken
    
    def update(self):
        """Update component each tick. By default, does nothing special."""
        if not self.operational:
            return
        # If exceeding maintenance interval, degrade condition

    
    def repair(self):
        """Full repair: restore to full condition."""
        self.condition = 1.0
        self.operational = True

