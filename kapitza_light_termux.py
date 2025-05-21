
import os

# Config
selected_mode = "endurance"
chosen_electrode = "Lead (Pb)"
chosen_electrolyte = "Sulfuric Acid (H2SO4)"

electrode_materials = {
    'Lead (Pb)': {'voltage_per_cell': 2.0},
    'Graphene': {'voltage_per_cell': 3.0},
    'Copper': {'voltage_per_cell': 1.5},
    'Aluminum': {'voltage_per_cell': 1.8},
    'Zinc': {'voltage_per_cell': 1.6},
    'Nickel': {'voltage_per_cell': 1.4}
}

electrolytes = {
    'Sulfuric Acid (H2SO4)': {'resistivity': 0.8},
    'Sodium Hydroxide (NaOH)': {'resistivity': 0.5},
    'Salt Water': {'resistivity': 2.0},
    'Potassium Hydroxide (KOH)': {'resistivity': 0.4},
    'Hydrochloric Acid (HCl)': {'resistivity': 1.0},
    'Phosphoric Acid': {'resistivity': 1.5}
}

def simulate(electrode, electrolyte, area_cm2, gap_mm, cells):
    area_m2 = area_cm2 / 1e4
    gap_m = gap_mm / 1000
    voltage_per_cell = electrode_materials[electrode]['voltage_per_cell']
    resistivity = electrolytes[electrolyte]['resistivity']

    resistance = resistivity * gap_m / area_m2
    voltage = voltage_per_cell * cells
    current = voltage / resistance
    power = voltage * current
    charge_time = (area_m2 * 3600) / (voltage * 1000)

    line = f"{electrode},{electrolyte},{area_cm2},{gap_mm},{cells},{voltage:.2f},{resistance:.4f},{current:.1f},{power:.1f},{charge_time:.3f}"

    if selected_mode == "endurance":
        energy_Wh = 1.5 * (area_cm2 / 100) * cells
        energy_J = energy_Wh * 3600
        duration_s = energy_J / power if power > 0 else 0
        line += f",{energy_Wh:.2f},{energy_J:.2f},{duration_s:.2f}"
    return line

areas = [400, 800, 1200]
gaps = [0.5, 1.0, 2.0]
cells_list = [3, 6]

header = "Electrode,Electrolyte,Plate Area (cm2),Plate Gap (mm),Cells,Voltage (V),Resistance (Ohm),Max Current (A),Power (W),Charge Time (min)"
if selected_mode == "endurance":
    header += ",Energy (Wh),Energy (J),Duration (s)"

results = [header]

for area in areas:
    for gap in gaps:
        for cells in cells_list:
            results.append(simulate(chosen_electrode, chosen_electrolyte, area, gap, cells))

# Print results
for line in results:
    print(line)

# Save to file
with open("kapitza_light_output.csv", "w") as f:
    f.write("\n".join(results))

print("\nSaved to kapitza_light_output.csv")
