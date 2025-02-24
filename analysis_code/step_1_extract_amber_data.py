import pandas as pd
import glob
import sys
import os
import gc  # Import garbage collector

# Set time conversion factors
time_units = {'NS': 0.001, 'PS': 1.0}  # Conversion factor from ps

# Get options from command-line arguments
if len(sys.argv) >= 4:
    drift_option = sys.argv[1]   # 'drift' or 'no_drift'
    time_unit = sys.argv[2].upper()  # 'NS' or 'PS'
    energy_components = sys.argv[3:]
else:
    print("Usage: python step_1_extract_amber_data.py <drift|no_drift> <NS|PS> <Energy Components>")
    print("Example: python step_1_extract_amber_data.py drift NS Etot_1")
    sys.exit(1)

# Validate drift option
if drift_option not in ['drift', 'no_drift']:
    print("Error: The first argument must be 'drift' or 'no_drift'.")
    sys.exit(1)

# Validate time unit
if time_unit not in time_units:
    print("Error: The second argument must be 'NS' or 'PS'.")
    sys.exit(1)

# Set time conversion factor based on time unit
time_conversion_factor = time_units[time_unit]
time_unit_label = f'Time ({time_unit.lower()})'
time_axis_title = f'Time ({time_unit.lower()})'

# Array of lambda values (adjust as necessary)
lambda_values = ['0.00000000', '0.25000000', '0.50000000', '0.75000000', '1.00000000']

# Function to extract the relevant energy data from the lines
def extract_energy_data(lines_iter):
    try:
        # Extract Etot, EKtot, EPtot
        etot_line = next(lines_iter)
        etot = float(etot_line.split('Etot')[1].split('=')[1].split()[0])
        ektot = float(etot_line.split('EKtot')[1].split('=')[1].split()[0])
        eptot = float(etot_line.split('EPtot')[1].split('=')[1].split()[0])

        # Extract BOND, ANGLE, DIHED
        bond_angle_line = next(lines_iter)
        bond = float(bond_angle_line.split('BOND')[1].split('=')[1].split()[0])
        angle = float(bond_angle_line.split('ANGLE')[1].split('=')[1].split()[0])
        dihed = float(bond_angle_line.split('DIHED')[1].split('=')[1].split()[0])

        # Extract 1-4 NB, 1-4 EEL, VDWAALS
        nb_elec_line = next(lines_iter)
        nb_14 = float(nb_elec_line.split('1-4 NB')[1].split('=')[1].split()[0])
        eel_14 = float(nb_elec_line.split('1-4 EEL')[1].split('=')[1].split()[0])
        vdwaals = float(nb_elec_line.split('VDWAALS')[1].split('=')[1].split()[0])

        # Extract EELEC, EHBOND
        elec_bond_line = next(lines_iter)
        eelec = float(elec_bond_line.split('EELEC')[1].split('=')[1].split()[0])
        ehbond = float(elec_bond_line.split('EHBOND')[1].split('=')[1].split()[0])

        # Skip lines until 'DV/DL' is found
        dv_dl = None
        for line in lines_iter:
            if 'DV/DL' in line:
                dv_dl = float(line.split('DV/DL')[1].split('=')[1].split()[0])
                break

        if dv_dl is None:
            print("Warning: 'DV/DL' not found.")
            return None

        return {
            'Etot': etot, 'EKtot': ektot, 'EPtot': eptot,
            'BOND': bond, 'ANGLE': angle, 'DIHED': dihed,
            'NB_14': nb_14, 'EEL_14': eel_14, 'VDWAALS': vdwaals,
            'EELEC': eelec, 'EHBOND': ehbond, 'DV/DL': dv_dl
        }
    except (ValueError, IndexError, StopIteration):
        return None

# Iterate over each energy component
for col in energy_components:
    # Iterate through each lambda value
    for lam in lambda_values:
        # File paths for the current lambda value
        file_paths = glob.glob(f'../{lam}_nve_*.mdout')

        # Sort file_paths numerically based on time steps
        def extract_time_step(file_path):
            try:
                time_step_str = file_path.split('_')[-1].split('.mdout')[0]
                return float(time_step_str)
            except ValueError:
                print(f"Warning: Could not extract time step from file path '{file_path}'. Assigning 0.0.")
                return 0.0

        file_paths.sort(key=extract_time_step)

        # Iterate through each file
        for file_path in file_paths:
            # Extract time step value from the file name
            time_step_str = file_path.split('_')[-1].split('.mdout')[0]

            # Initialize lists to store TIME and energy data for this file
            times = []
            energies = []

            # Open the file and process line by line
            with open(file_path, 'r') as file:
                lines_iter = iter(file)
                for line in lines_iter:
                    # Stop extracting when encountering the "A V E R A G E S   O V E R" line
                    if "A V E R A G E S   O V E R" in line:
                        break

                    if 'TIME(PS)' in line:
                        try:
                            # Find the value after 'TIME(PS) ='
                            time_value_ps = float(line.split('TIME(PS) =')[1].split()[0])
                            # Convert time from ps to desired unit
                            time_value = time_value_ps * time_conversion_factor

                            # Extract data for TI region 1
                            data_region_1 = extract_energy_data(lines_iter)

                            # Skip lines until next 'TIME(PS)' or end of file
                            while True:
                                line = next(lines_iter, None)
                                if line is None or 'TIME(PS)' in line:
                                    break

                            # Extract data for TI region 2
                            data_region_2 = extract_energy_data(lines_iter) if line else None

                            # Determine the TI region from the component name
                            if col.endswith('_1'):
                                region = 1
                                comp_name = col[:-2]  # Remove '_1'
                                data_region = data_region_1
                            elif col.endswith('_2'):
                                region = 2
                                comp_name = col[:-2]  # Remove '_2'
                                data_region = data_region_2
                            else:
                                print(f"Error: Energy component '{col}' must end with '_1' or '_2'.")
                                sys.exit(1)

                            # Get the energy value
                            if data_region and comp_name in data_region:
                                energy_value = data_region[comp_name]
                            else:
                                energy_value = float('nan')

                            times.append(time_value)
                            energies.append(energy_value)

                        except (ValueError, IndexError, StopIteration) as e:
                            continue

            # If no data was collected, skip to next file
            if not times or not energies:
                print(f"No data collected for time step {time_step_str} in lambda {lam}. Skipping.")
                continue

            # Create a DataFrame for this time step
            df = pd.DataFrame({'Time': times, col: energies})

            # Sort df by Time
            df.sort_values(by='Time', inplace=True)

            # Determine whether to process drift or actual energies
            if drift_option == 'drift':
                # Subtract the initial energy value (at time=0) from all energies to calculate drift
                initial_energy = df.iloc[0][col]
                df[col] = df[col] - initial_energy

            # Drop NaN values
            df_nonan = df[['Time', col]].dropna()
            if df_nonan.empty:
                print(f"No valid data for {col} at time step {time_step_str} in lambda {lam}. Skipping.")
                continue

            # Rename 'Time' to '#Time' before saving
            df_to_save = df_nonan.copy()
            df_to_save.rename(columns={'Time': '#Time'}, inplace=True)

            # Save the energy data to file
            sanitized_col = col.replace('/', '_')
            filename = f"{lam}_{time_step_str}_{sanitized_col}_{drift_option}.dat"
            df_to_save.to_csv(filename, index=False, sep='\t', float_format='%.8f')
            print(f"Energy data saved to {filename}")

            # After processing, delete df and other variables to free memory
            del df, df_nonan, times, energies, df_to_save
            gc.collect()  # Force garbage collection

# Debug: Print the available time steps for each lambda, sorted numerically
for lam in lambda_values:
    print(f"Lambda {lam}: Available time steps processed.")

