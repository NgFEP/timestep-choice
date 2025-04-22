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
lambda_values = ['0.00000000']

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
    print("Usage: python analyze_energy_data.py <start> <end> <skip> <image|no_image> <Energy Component>")
    print("Example: python analyze_energy_data.py 0.0 10.0 10 image Etot_1")
    sys.exit(1)

# Validate image option
if image_option not in ['image', 'no_image']:
    print("Error: The fourth argument must be 'image' or 'no_image'.")
    sys.exit(1)

# If drift_option is needed, define it here or get from command-line arguments
drift_option = 'drift'  # or 'no_drift', depending on your files

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

# Initialize list to collect slopes for all lambdas
all_slopes = []

# Iterate over each lambda value
for lam in lambda_values:
    lambda_value = float(lam)
    # Initialize a dict to store slopes for this lambda
    lambda_slopes = {'Lambda': lambda_value}

    # Initialize a list to store regression parameters for this lambda
    regression_results = []

    # Initialize figure for plotting for this lambda
    fig = go.Figure()

    # Color index for the color palette
    color_index = 0  # To iterate over colors

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

        # Get color for this dt value
        color = color_palette[color_index % len(color_palette)]
        color_index += 1  # Increment color index

        # Plot data points
        fig.add_trace(go.Scatter(
            x=df_nonan['Time'],
            y=df_nonan[energy_component],
            mode='markers',
            opacity=0.25,
            name=f'{energy_component} (dt={dt})',
            marker=dict(color=color)
        ))

        # Perform linear regression on the energy component vs Time
        slope, intercept, r_value, p_value, std_err = linregress(df_nonan['Time'], df_nonan[energy_component])

        # Calculate R-squared
        r_squared = r_value ** 2

        # Calculate standard deviation of the energy component
        std_dev = np.std(df_nonan[energy_component])

        # Store regression parameters
        regression_results.append({
            'Lambda': lam,
            'dt': float(dt),
            'Energy Component': energy_component,
            'Slope': slope,
            'Intercept': intercept,
            'R-value': r_value,
            'P-value': p_value,
            'Std Err': std_err,
            'R-squared': r_squared,
            'Standard Deviation': std_dev,
            'Start Time': current_start_time,
            'End Time': current_end_time,
            'Min Time': data_start_time,
            'Max Time': data_end_time
        })

        # Store the slope in lambda_slopes
        dt_label = dt_mapping.get(dt)
        if dt_label is None:
            print(f"Warning: dt value {dt} not in dt_mapping.")
            continue
        lambda_slopes[f'dt={dt_label}'] = slope

        # Print the results
        print(f"Results for {energy_component} at dt {dt} (lambda {lam}):")
        print(f"  Slope = {slope}")
        print(f"  Intercept = {intercept}")
        print(f"  R-value = {r_value}")
        print(f"  P-value = {p_value}")
        print(f"  Std Err = {std_err}")
        print(f"  R-squared = {r_squared}")
        print(f"  Standard Deviation = {std_dev}\n")

        # Compute regression line values
        regression_line = intercept + slope * df_nonan['Time']

        # Add regression line to plot with slope in the legend
        fig.add_trace(go.Scatter(
            x=df_nonan['Time'],
            y=regression_line,
            mode='lines',
            name=f'Regression Line (dt={dt}, Slope={slope:.2e})',
            line=dict(dash='dash', color=color)
        ))

        # After processing, delete df and other variables to free memory
        del df, df_nonan
        gc.collect()  # Force garbage collection

    # After processing all dt_values for this lambda, save the regression results
    if regression_results:
        regression_results_df = pd.DataFrame(regression_results)
        regression_results_df.sort_values(by=['Energy Component', 'Lambda', 'dt'], inplace=True)

        for index, result in regression_results_df.iterrows():
            print(f"Lambda {result['Lambda']}, dt {result['dt']}, Energy Component {result['Energy Component']}, "
                  f"Start Time: {result['Start Time']}, End Time: {result['End Time']}")
            print(f"  Slope = {result['Slope']}")
            print(f"  Intercept = {result['Intercept']}")
            print(f"  R-value = {result['R-value']}")
            print(f"  P-value = {result['P-value']}")
            print(f"  Std Err = {result['Std Err']}")
            print(f"  R-squared = {result['R-squared']}")
            print(f"  Standard Deviation = {result['Standard Deviation']}\n")

        # Save regression results to a CSV file with lambda value in the filename
        sanitized_component = energy_component.replace('/', '_')
        csv_filename = f"{lam}_energy_regression_results_{sanitized_component}_start_{start_time}_end_{end_time}.csv"
        regression_results_df.to_csv(csv_filename, index=False)
        print(f"Regression results saved to {csv_filename}")
    else:
        print(f"No regression results to save for lambda {lam}.")

    # Append the collected slopes for this lambda to the all_slopes list
    all_slopes.append(lambda_slopes)

    # Save the plot if image_option is 'image'
    if image_option == 'image':
        # Set plot titles
        fig.update_layout(
            title=f'{energy_component} vs Time (Lambda {lam})',
            xaxis_title='Time (ns)',
            yaxis_title=f'{energy_component} (kcal/mol)',
            legend_title="dt Values",
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

        # Add slope annotations to the plot
        if regression_results:
            # Iterate over regression results to add annotations
            for index, result in regression_results_df.iterrows():
                dt_value = result['dt']
                slope_value = result['Slope']
                intercept_value = result['Intercept']
                # Use the end time for x position of annotation
                x_pos = result['End Time']
                y_pos = intercept_value + slope_value * x_pos
                color = color_palette[index % len(color_palette)]

                # Add annotation to the plot
                fig.add_annotation(
                    x=x_pos,
                    y=y_pos,
                    text=f"Slope={slope_value:.2e}",
                    showarrow=True,
                    arrowhead=1,
                    ax=0,
                    ay=-40,
                    font=dict(color=color),
                    bgcolor='rgba(255,255,255,0.5)',  # Semi-transparent background
                    bordercolor=color
                )

        # Save the plot with lambda value in the filename
        sanitized_component = energy_component.replace('/', '_')
        plot_filename = f'{lam}_{sanitized_component}_start_{start_time}_end_{end_time}'

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

# After processing all lambdas, create DataFrame from all_slopes
all_slopes_df = pd.DataFrame(all_slopes)

# Arrange columns in the desired order
all_slopes_df = all_slopes_df[columns_order]

# Define a function to format the slopes for LaTeX
def format_slope(value):
    if pd.isnull(value):
        return ''
    elif value == 0:
        return '0'
    else:
        exponent = int(np.floor(np.log10(abs(value))))
        mantissa = value / (10 ** exponent)
        # Format mantissa with one decimal place
        mantissa_str = f'{mantissa:.1f}'
        # Format for LaTeX: $7.7 \times 10^{-2}$
        # Escape backslashes for CSV
        return f'${mantissa_str} \\times 10^{{{exponent}}}$'

# Apply the formatting function to the slope columns
slope_columns = [col for col in all_slopes_df.columns if col != 'Lambda']
for col in slope_columns:
    all_slopes_df[col] = all_slopes_df[col].apply(format_slope)

# Save the DataFrame to '${sanitized_component}_all_lambda_slope.csv' without index
all_slopes_df.to_csv(f'{sanitized_component}_all_lambda_slope.csv', index=False)
print(f"All slopes have been saved to {sanitized_component}_all_lambda_slope.csv")

