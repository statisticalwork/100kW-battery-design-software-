
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Electrode materials
electrode_materials = {
    'Lead (Pb)': {'conductivity': 4.8e6, 'voltage_per_cell': 2.0},
    'Graphene': {'conductivity': 1.0e8, 'voltage_per_cell': 3.0},
    'Copper': {'conductivity': 5.8e7, 'voltage_per_cell': 1.5},
    'Aluminum': {'conductivity': 3.8e7, 'voltage_per_cell': 1.8},
    'Zinc': {'conductivity': 1.7e7, 'voltage_per_cell': 1.6},
    'Nickel': {'conductivity': 1.4e7, 'voltage_per_cell': 1.4}
}

# Electrolytes
electrolytes = {
    'Sulfuric Acid (H2SO4)': {'resistivity': 0.8},
    'Sodium Hydroxide (NaOH)': {'resistivity': 0.5},
    'Salt Water': {'resistivity': 2.0},
    'Potassium Hydroxide (KOH)': {'resistivity': 0.4},
    'Hydrochloric Acid (HCl)': {'resistivity': 1.0},
    'Phosphoric Acid': {'resistivity': 1.5}
}

def choose_option(prompt, options):
    print(prompt)
    for i, key in enumerate(options):
        print(f"{i + 1}. {key}")
    while True:
        try:
            idx = int(input("Select number: ")) - 1
            if 0 <= idx < len(options):
                return list(options.keys())[idx]
        except ValueError:
            pass
        print("Invalid selection. Try again.")

# User selections
chosen_electrode = choose_option("Choose Electrode Material:", electrode_materials)
chosen_electrolyte = choose_option("Choose Electrolyte:", electrolytes)

# Plate diameter input
try:
    plate_diameter_cm = float(input("Enter plate diameter in cm (round): "))
    plate_area_cm2 = 3.1416 * (plate_diameter_cm / 2) ** 2
except:
    plate_area_cm2 = 1200

# Mode
selected_mode = input("Choose mode (power or endurance): ").strip().lower()
if selected_mode not in ["power", "endurance"]:
    selected_mode = "endurance"

# Simulation function
def battery_simulation(electrode, electrolyte, plate_area_cm2, plate_gap_mm, num_cells, mode="power"):
    plate_area_m2 = plate_area_cm2 / 1e4
    plate_gap_m = plate_gap_mm / 1000
    voltage_per_cell = electrode_materials[electrode]['voltage_per_cell']
    resistivity = electrolytes[electrolyte]['resistivity']
    resistance = resistivity * plate_gap_m / plate_area_m2
    voltage = voltage_per_cell * num_cells
    max_current = voltage / resistance
    power_output = voltage * max_current
    charge_time = (plate_area_m2 * 3600) / (voltage * 1000)

    result = {
        'Electrode': electrode,
        'Electrolyte': electrolyte,
        'Plate Area (cm²)': plate_area_cm2,
        'Plate Gap (mm)': plate_gap_mm,
        'Cells': num_cells,
        'Voltage (V)': voltage,
        'Resistance (Ohms)': resistance,
        'Max Current (A)': max_current,
        'Power Output (W)': power_output,
        'Approx. Charge Time (min)': charge_time
    }

    if mode == "endurance":
        energy_Wh = 1.5 * (plate_area_cm2 / 100) * num_cells
        energy_J = energy_Wh * 3600
        duration_s = energy_J / power_output if power_output > 0 else 0
        result['Estimated Energy (Wh)'] = energy_Wh
        result['Estimated Energy (J)'] = energy_J
        result['Estimated Discharge Duration (s)'] = duration_s

    return result

# Configurations to test
plate_gaps_mm = [0.5, 1, 2]
cell_counts = [3, 6, 9]

results = []
for gap in plate_gaps_mm:
    for cells in cell_counts:
        r = battery_simulation(chosen_electrode, chosen_electrolyte, plate_area_cm2, gap, cells, selected_mode)
        results.append(r)

df = pd.DataFrame(results)

# Save plots
output_folder = "kapitza_battery_plots"
os.makedirs(output_folder, exist_ok=True)

# Plot 1: Energy vs Power Output
if "Estimated Energy (Wh)" in df.columns:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="Estimated Energy (Wh)", y="Power Output (W)", hue="Plate Gap (mm)", palette="viridis")
    plt.title("Energy Capacity vs Power Output")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/energy_vs_power.png")

# Plot 2: Discharge Duration vs Resistance
if "Estimated Discharge Duration (s)" in df.columns:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="Resistance (Ohms)", y="Estimated Discharge Duration (s)", hue="Cells", palette="magma")
    plt.title("Resistance vs Discharge Duration")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/resistance_vs_duration.png")

# Plot 3: Power Output by Plate Gap
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x="Plate Gap (mm)", y="Power Output (W)")
plt.title("Power Output by Plate Gap")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_folder}/power_by_gap.png")

# Plot 4: Charge Time by Cell Count
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x="Cells", y="Approx. Charge Time (min)")
plt.title("Charge Time by Number of Cells")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_folder}/charge_time_by_cells.png")

# Save to CSV
df.to_csv("kapitza_interactive_output.csv", index=False)
print("Simulation complete. Results saved to CSV and plots folder.")
