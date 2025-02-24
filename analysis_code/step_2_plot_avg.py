import pandas as pd
import glob
import sys
import os
import gc  # Import garbage collector
from scipy.stats import linregress
import numpy as np
import plotly.graph_objects as go
import plotly.express as px  # Import plotly express for color palettes
import re  # Import the regular expressions module

# Array of lambda values (adjust as necessary)
lambda_values = ['0.00000000', '0.25000000', '0.50000000', '0.75000000', '1.00000000']

# List of dt_values (time step values), adjust as necessary
dt_values = ['0.0005', '0.001', '0.002', '0.0025', '0.00333333', '0.004']

# Mapping of dt_values to desired dt labels
dt_mapping = {
    '0.0005': '0.5',
    '0.001': '1',
    '0.002': '2',
    '0.0025': '2.5',
    '0.00333333': '3.3333',
    '0.004': '4'
}

# Desired column order for the output CSV
columns_order = ['Lambda', 'dt=0.5', 'dt=1', 'dt=2', 'dt=2.5', 'dt=3.3333', 'dt=4']

# Get options from command-line arguments
if len(sys.argv) >= 6:
    # Handle 'start' and 'last' as special arguments
    if sys.argv[1].lower() == 'start':
        start_time = None
    else:
        try:
            start_time = float(sys.argv[1])
        except ValueError:
            print("Error: Start time must be a number or 'start'")
            sys.exit(1)
    if sys.argv[2].lower() in ['end', 'last']:
        end_time = None
    else:
        try:
            end_time = float(sys.argv[2])
        except ValueError:
            print("Error: End time must be a number or 'end' or 'last'")
            sys.exit(1)
    try:
        skip_value = int(sys.argv[3])
        if skip_value <= 0:
            raise ValueError
    except ValueError:
        print("Error: Skip value must be a positive integer.")
        sys.exit(1)
    image_option = sys.argv[4]
    energy_component = sys.argv[5]
    sanitized_component = energy_component.replace('/', '_')  # Sanitize the energy component
else:
    print("Usage: python step_2_plot_avg.py <start> <end> <skip> <image|no_image> <Energy Component>")
    print("Example: python step_2_plot_avg.py 0.0 10.0 10 image Etot_1")
    sys.exit(1)

# Validate image option
if image_option not in ['image', 'no_image']:
    print("Error: The fourth argument must be 'image' or 'no_image'.")
    sys.exit(1)

# If drift_option is needed, define it here or get from command-line arguments
drift_option = 'no_drift'  # or 'no_drift', depending on your files

# Use the 'Dark24' color palette from Plotly
color_palette = px.colors.qualitative.Dark24

# Import the font size and dimensions for consistency
dpi = 300
desired_width_in_inches = 3 
desired_height_in_inches = 3
image_width = desired_width_in_inches * dpi
image_height = desired_height_in_inches * dpi

# Set font name and tick font size
fontname = "Times New Roman"
tick_font_size = 14
axis_font_size = 24

# Initialize list to collect averages for all lambdas
all_averages = []

# Iterate over each lambda value
for lam in lambda_values:
    lambda_value = float(lam)
    # Initialize a dict to store averages for this lambda
    lambda_averages = {'Lambda': lambda_value}

    # Initialize a list to store average results for this lambda
    avg_results = []

    # Initialize lists for plotting
    dt_labels = []
    avg_values = []
    std_values = []

    # Iterate over each dt value
    for dt in dt_values:
        # Build the file pattern for the current lambda, dt, and energy component
        sanitized_component = energy_component.replace('/', '_')
        pattern = f"{lam}_{dt}_{sanitized_component}_{drift_option}.dat"
        file_paths = glob.glob(pattern)

        # If no files match the pattern, skip to next dt
        if not file_paths:
            print(f"No files found for pattern {pattern}. Skipping.")
            continue

        # There should be one file per pattern; use the first one
        file_path = file_paths[0]

        # Read the data file
        df = pd.read_csv(file_path, sep='\t')

        # Rename '#Time' back to 'Time' for processing
        df.rename(columns={'#Time': 'Time'}, inplace=True)

        # Drop NaN values
        df_nonan = df[['Time', energy_component]].dropna()
        if df_nonan.empty:
            print(f"No valid data in file {file_path}. Skipping.")
            continue

        # Handle 'start' and 'last' for start_time and end_time
        data_start_time = df_nonan['Time'].min()
        data_end_time = df_nonan['Time'].max()

        # Set start_time and end_time if they are None
        if start_time is None:
            current_start_time = data_start_time
        else:
            current_start_time = start_time

        if end_time is None:
            current_end_time = data_end_time
        else:
            current_end_time = end_time

        # Filter data based on start and end times
        df_nonan = df_nonan[(df_nonan['Time'] >= current_start_time) & (df_nonan['Time'] <= current_end_time)]

        if df_nonan.empty:
            print(f"No valid data in file {file_path} within the specified time range. Skipping.")
            continue

        # Apply skip value to read data at specified intervals
        df_nonan = df_nonan.iloc[::skip_value]

        # Calculate average and standard deviation of the energy component
        average_value = df_nonan[energy_component].mean()
        std_dev = df_nonan[energy_component].std()

        # Store average results
        avg_results.append({
            'Lambda': lam,
            'dt': float(dt),
            'dt_label': dt_mapping.get(dt, dt),
            'Energy Component': energy_component,
            'Average': average_value,
            'Standard Deviation': std_dev
        })

        # Store the average in lambda_averages
        dt_label = dt_mapping.get(dt)
        if dt_label is None:
            print(f"Warning: dt value {dt} not in dt_mapping.")
            continue
        lambda_averages[f'dt={dt_label}'] = average_value

        # Collect data for plotting
        dt_labels.append(dt_label)
        avg_values.append(average_value)
        std_values.append(std_dev)

        # Print the results
        print(f"Results for {energy_component} at dt {dt} (lambda {lam}):")
        print(f"  Average = {average_value}")
        print(f"  Standard Deviation = {std_dev}\n")

        # After processing, delete df and other variables to free memory
        del df, df_nonan
        gc.collect()  # Force garbage collection

    # After processing all dt_values for this lambda, save the average results
    if avg_results:
        avg_results_df = pd.DataFrame(avg_results)
        avg_results_df.sort_values(by=['Energy Component', 'Lambda', 'dt'], inplace=True)

        for index, result in avg_results_df.iterrows():
            print(f"Lambda {result['Lambda']}, dt {result['dt']}, Energy Component {result['Energy Component']}")
            print(f"  Average = {result['Average']}")
            print(f"  Standard Deviation = {result['Standard Deviation']}\n")

        # Save average results to a CSV file with lambda value in the filename
        sanitized_component = energy_component.replace('/', '_')
        csv_filename = f"{lam}_energy_avg_results_{sanitized_component}_start_{start_time}_end_{end_time}.csv"
        # Exclude unwanted columns
        avg_results_df = avg_results_df[['Lambda', 'dt', 'dt_label', 'Energy Component', 'Average', 'Standard Deviation']]
        avg_results_df.to_csv(csv_filename, index=False)
        print(f"Average results saved to {csv_filename}")
    else:
        print(f"No average results to save for lambda {lam}.")

    # Append the collected averages for this lambda to the all_averages list
    all_averages.append(lambda_averages)

    # Save the plot if image_option is 'image'
    if image_option == 'image':
        # Create a bar chart with error bars
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=dt_labels,
            y=avg_values,
            error_y=dict(type='data', array=std_values, visible=True),
            name=f'Lambda {lam}',
            marker_color=color_palette[0]
        ))

        # Set plot titles and layout
        fig.update_layout(
            title=f'Average {energy_component} vs dt (Lambda {lam})',
            xaxis_title='dt (fs)',
            yaxis_title=f'Average {energy_component} (kcal/mol)',
            font=dict(
                family=fontname,
                size=tick_font_size
            ),
            xaxis=dict(
                title_font=dict(size=axis_font_size),
                tickfont=dict(size=tick_font_size)
            ),
            yaxis=dict(
                title_font=dict(size=axis_font_size),
                tickfont=dict(size=tick_font_size)
            )
        )

        # Save the plot with lambda value in the filename
        sanitized_component = energy_component.replace('/', '_')
        plot_filename = f'{lam}_{sanitized_component}_avg_bar_chart_start_{start_time}_end_{end_time}'

        fig.write_html(f'{plot_filename}.html')
        fig.write_image(
            f'{plot_filename}.png',
            width=image_width,
            height=image_height,
            scale=1
        )
        print(f"Plot saved as {plot_filename}.html and {plot_filename}.png")
    else:
        print("Image saving is disabled. Skipping saving plot images.")

    # Delete figure to free up memory
    del fig
    gc.collect()

# After processing all lambdas, create DataFrame from all_averages
all_averages_df = pd.DataFrame(all_averages)

# Arrange columns in the desired order
all_averages_df = all_averages_df[['Lambda'] + [col for col in all_averages_df.columns if col != 'Lambda']]

# Save the DataFrame to '${sanitized_component}_all_lambda_averages.csv' without index
all_averages_df.to_csv(f'{sanitized_component}_all_lambda_averages.csv', index=False)
print(f"All averages have been saved to {sanitized_component}_all_lambda_averages.csv")

