import math

# Constants
HENRY_CONSTANT_CO2_AT_25C = 29.41  # ppm/atm at 25°C
HENRY_CONSTANT_TEMP_COEFFICIENT = -0.4  # ppm/atm per °C

def co2_scrubber_room_concentration(
    inlet_co2_concentration_ppm,
    scrubber_flow_rate_m3_per_min,
    scrubber_volume_m3,
    solution_volume_liters,
    temperature_celsius,
    pressure_atm,
    time_minutes,
    room_size_m3
):
    """
    Calculates the CO₂ concentration in the room, total CO₂ removed, and instantaneous ppm removal rate.
    """
    
    # Safety checks
    assert scrubber_flow_rate_m3_per_min > 0, "Flow rate must be positive."
    assert solution_volume_liters > 0, "Solution volume must be positive."
    assert room_size_m3 > 0, "Room size must be positive."
    
    # 1. Convert solution volume to cubic meters
    solution_volume_m3 = solution_volume_liters / 1000  # m³
    
    # 2. Residence Time (tau)
    residence_time_min = scrubber_volume_m3 / scrubber_flow_rate_m3_per_min  # minutes
    
    # 3. Henry's Law Constant Adjustment
    H_adjusted = (HENRY_CONSTANT_CO2_AT_25C + HENRY_CONSTANT_TEMP_COEFFICIENT * (temperature_celsius - 25)) * pressure_atm
    H_adjusted = max(H_adjusted, 0.1)  # Prevent negative or zero values
    
    # 4. Effective Henry's Law Constant
    H_eff = H_adjusted * residence_time_min  # ppm·min/atm
    
    # 5. Steady-State CO₂ Concentration (C_ss)
    C_ss = inlet_co2_concentration_ppm / (1 + (H_eff * solution_volume_m3) / scrubber_flow_rate_m3_per_min)
    
    # 6. Rate Constant (k)
    k = (H_eff * solution_volume_m3) / (room_size_m3 * (1 + (H_eff * solution_volume_m3) / scrubber_flow_rate_m3_per_min))  # 1/min
    
    # 7. Room CO₂ Concentration at Time t (C_t)
    C_t = C_ss + (inlet_co2_concentration_ppm - C_ss) * math.exp(-k * time_minutes)  # ppm
    
    # 8. Total CO₂ Removed and Removal Rate
    ppm_removed_total = inlet_co2_concentration_ppm - C_t  # ppm
    ppm_removal_rate_ppm_per_min = k * (C_t - C_ss)  # ppm/min
    
    return C_t, ppm_removed_total, ppm_removal_rate_ppm_per_min

# Example Usage
if __name__ == "__main__":
    # Inputs
    inlet_co2_concentration_ppm = 1000  # ppm
    scrubber_flow_rate_m3_per_min = 150  # m³/min
    scrubber_volume_m3 = 12  # m³
    solution_volume_liters = 6000  # liters
    temperature_celsius = 30  # °C
    pressure_atm = 1.0  # atm
    time_minutes = 200  # minutes
    room_size_m3 = 500  # m³
    
    # Calculate room CO₂ concentration, total removal, and removal rate
    room_co2_ppm, ppm_removed, ppm_removal_rate = co2_scrubber_room_concentration(
        inlet_co2_concentration_ppm,
        scrubber_flow_rate_m3_per_min,
        scrubber_volume_m3,
        solution_volume_liters,
        temperature_celsius,
        pressure_atm,
        time_minutes,
        room_size_m3
    )
    
    # Outputs
    print("\nCO₂ Scrubber Performance Model")
    print("--------------------------------")
    print(f"Initial Room CO₂ Concentration: {inlet_co2_concentration_ppm} ppm")
    print(f"Room Size: {room_size_m3} m³")
    print(f"Scrubber Flow Rate: {scrubber_flow_rate_m3_per_min} m³/min")
    print(f"Solution Volume: {solution_volume_liters} liters ({solution_volume_liters / 1000:.2f} m³)")
    print(f"Operating Temperature: {temperature_celsius} °C")
    print(f"Operating Pressure: {pressure_atm} atm")
    print(f"Time Elapsed: {time_minutes} minutes\n")
    
    print(f"Henry's Law Constant (Adjusted): {H_adjusted:.2f} ppm/atm")
    print(f"Residence Time: {residence_time_min:.2f} minutes")
    print(f"Effective Henry's Law Constant (H_eff): {H_eff:.2f} ppm·min/atm")
    print(f"Steady-State CO₂ Concentration (C_ss): {C_ss:.2f} ppm")
    print(f"Rate Constant (k): {k:.6f} 1/min\n")
    print(f"CO₂ Concentration in Room: {room_co2_ppm:.2f} ppm")
    print(f"Total CO₂ Removed: {ppm_removed:.2f} ppm")
    print(f"Instantaneous CO₂ Removal Rate: {ppm_removal_rate:.2f} ppm/min")
