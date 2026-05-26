def energy_consumed(mass_kg, T_process, T_initial, Cp=3.93):
    delta_T = T_process - T_initial
    energy_kj = mass_kg * Cp * delta_T
    energy_kwh = energy_kj / 3600
    return round(energy_kwh, 4)

def cost_saved(T_optimal, t_optimal, T_overprocess, t_overprocess, 
               mass_kg, T_initial, Cp, tariff):
    energy_optimal = energy_consumed(mass_kg, T_optimal, T_initial, Cp)
    energy_over = energy_consumed(mass_kg, T_overprocess, T_initial, Cp)
    energy_diff = energy_over - energy_optimal
    saving = energy_diff * tariff
    return round(energy_diff, 4), round(saving, 2)