# entities/components.py



class Component:
    def __init__(self, name):
        self.name = name
        self.operational = True
        self.condition = 1.0  # 1.0 = perfect condition, 0.0 = broken
        self.maintenance_interval = 10000  # ticks between maintenance
        self.time_since_maintenance = 0
    
    def update(self, dt, resources, environment):
        """Update component each tick. By default, does nothing special."""
        if not self.operational:
            return
        self.time_since_maintenance += dt
        # If exceeding maintenance interval, degrade condition
        if self.time_since_maintenance > self.maintenance_interval:
            self.condition -= 0.001 * dt
            if self.condition <= 0:
                self.condition = 0
                self.operational = False
    
    def perform_maintenance(self):
        """Reset maintenance counter and restore some condition."""
        self.time_since_maintenance = 0
        self.condition = min(1.0, self.condition + 0.2)
        if self.condition > 0.2:
            self.operational = True
    
    def repair(self):
        """Full repair: restore to full condition."""
        self.condition = 1.0
        self.operational = True
        self.time_since_maintenance = 0

class CO2Scrubber(Component):
    def __init__(self, scrub_rate=5.0):
        super().__init__("CO2 Scrubber")
        self.scrub_rate = scrub_rate
    
    def update(self, dt, resources, environment):
        super().update(dt, resources, environment)
        if self.operational:
            # Reduce CO2 by scrub_rate * condition (if condition<1, less effective)
            reduction = self.scrub_rate * self.condition * dt
            resources["CO2"] = max(0, resources["CO2"] - reduction)

class O2Controller(Component):
    # Based on O2 Partial Pressure range [V2 6003]
    def __init__(self, desired_o2_pp=210.0):
        super().__init__("O2 Controller")
        self.desired_o2_pp = desired_o2_pp  # mmHg partial pressure
    
    def update(self, dt, resources, environment):
        super().update(dt, resources, environment)
        if self.operational:
            # If O2 partial pressure is off, adjust O2 resource
            # Convert O2 partial pressure to a rough approximation of how many L we need
            # For simplicity, assume resources["O2"] maps to partial pressure linearly.
            current_o2_pp = environment["o2_pp"]
            diff = self.desired_o2_pp - current_o2_pp
            # If diff > 0, add O2. If < 0, can't remove O2 easily, just let environment handle?
            if diff > 0:
                # Add O2 at a rate scaled by diff and condition
                add_amount = diff * 0.1 * self.condition * dt
                resources["O2"] = min(resources["O2"] + add_amount, 3360.0)  # capped by max
            # If too high O2, we do nothing or vent small amounts?
            if diff < 0:
                # Vent O2?
                remove_amount = abs(diff) * 0.05 * self.condition * dt
                resources["O2"] = max(0, resources["O2"] - remove_amount)

class PressureRegulator(Component):
    # Based on V2 6006 total pressure tolerance range.
    def __init__(self, target_pressure=1013.0):
        super().__init__("Pressure Regulator")
        self.target_pressure = target_pressure  # hPa

    def update(self, dt, resources, environment):
        super().update(dt, resources, environment)
        if self.operational:
            current_pressure = environment["pressure"]
            diff = self.target_pressure - current_pressure
            # If diff > 0, add inert gas or O2/N2 to raise pressure (V2 6002 inert diluent gas)
            # If diff < 0, vent gas
            if diff > 0:
                # Add inert gas (no resource count for it?), just assume stable
                # Possibly consume a generic "N2" from resources if defined.
                pass
            else:
                # Venting gas to lower pressure - we won't track that resource currently.
                pass

class HumidityController(Component):
    # Based on V2 6011 Post Landing RH, V2 6012 Crew Health Environmental Limits
    def __init__(self, desired_rh=50.0):
        super().__init__("Humidity Controller")
        self.desired_rh = desired_rh
    
    def update(self, dt, resources, environment):
        super().update(dt, resources, environment)
        if self.operational:
            # Adjust humidity toward desired_rh
            current_rh = environment["rh"]
            diff = self.desired_rh - current_rh
            # If diff > 0, add moisture (consume H2O)
            if diff > 0:
                consume_h2o = diff * 0.01 * self.condition * dt
                consume_h2o = min(consume_h2o, resources["H2O"]) 
                resources["H2O"] = max(0, resources["H2O"] - consume_h2o)
                # Increase rh slightly
                environment["rh"] += diff * 0.1 * self.condition * dt
            else:
                # Dehumidify by venting moisture (not tracked), reduce RH
                environment["rh"] += diff * 0.1 * self.condition * dt

class EnvironmentalMonitor(Component):
    # Based on V2 6020 (data recording), V2 6021 (displaying), V2 6022 (monitoring/alerting)
    def __init__(self):
        super().__init__("Environmental Monitor")
        self.data_log = []

    def update(self, dt, resources, environment):
        super().update(dt, resources, environment)
        if self.operational:
            # Record current environment data for trend analysis [V2 6001]
            record = {
                "time": dt,
                "O2": resources["O2"],
                "CO2": resources["CO2"],
                "pressure": environment["pressure"],
                "rh": environment["rh"],
                "o2_pp": environment["o2_pp"]
            }
            self.data_log.append(record)
            # If some parameter out of range, alert (not fully implemented)
    
    def display_data(self):
        # Example of V2 6021 data displaying
        if not self.data_log:
            return "No Data"
        recent = self.data_log[-1]
        return f"Env Data: O2:{recent['O2']}L, CO2:{recent['CO2']}ppm, P:{recent['pressure']}hPa, RH:{recent['rh']}%, O2_pp:{recent['o2_pp']}mmHg"

class VentilationController(Component):
    # V2 6107, V2 6108 Nominal and Off-Nominal Ventilation
    def __init__(self):
        super().__init__("Ventilation Controller")
    
    def update(self, dt, resources, environment):
        super().update(dt, resources, environment)
        if self.operational:
            # Ensure atmosphere is well mixed
            # Not implemented fully, just a placeholder
            pass
