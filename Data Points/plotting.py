import matplotlib.pyplot as plt

def plot_data(df, plot_type, time_col="data_point"):
    """
    Plots the selected sensor streams using the specified plot type.

    Parameters:
        df (pd.DataFrame): DataFrame containing the time column and sensor data.
        plot_type (str): Type of plot to generate ('line' or 'box').
        time_col (str): Name of the time/index column (default is 'data_point').
    """
    # Extract all stream columns (excluding the time/index column)
    streams = df.columns.drop(time_col)

    if plot_type == "line":
        # Create a line plot for each selected stream
        fig, ax = plt.subplots(figsize=(10, 5))
        for stream in streams:
            ax.plot(df[time_col], df[stream], label=stream)
        ax.set_title("Line Plot of Selected Streams")
        ax.set_xlabel("Data Point")
        ax.set_ylabel("Normalized Values")
        ax.legend()
        fig.tight_layout()
        plt.show()

    elif plot_type == "box":
        # Create a box plot to show distribution of values for each stream
        fig, ax = plt.subplots(figsize=(8, 5))
        df[streams].plot(kind='box', ax=ax)
        ax.set_title("Box Plot of Selected Streams")
        ax.set_ylabel("Normalized Value")
        ax.grid(True)
        plt.show()

    else:
        # Handle unsupported plot types
        print("Unsupported plot type selected.")
