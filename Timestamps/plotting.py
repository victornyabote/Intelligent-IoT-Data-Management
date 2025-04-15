import matplotlib.pyplot as plt

def plot_data(df, plot_type):
    """
    Plots the selected streams from the DataFrame using either a line plot or a box plot.

    Parameters:
        df (pd.DataFrame): Cleaned and normalized DataFrame with 'datetime' and one or more stream columns.
        plot_type (str): The type of plot to display ('line' or 'box').
    """
    # Extract stream column names (exclude 'datetime')
    streams = df.columns.drop('datetime')

    # Create a line plot for each selected stream
    if plot_type == "line":
        fig, ax = plt.subplots(figsize=(10, 5))  # Create figure and axis
        for stream in streams:
            ax.plot(df['datetime'], df[stream], label=stream)
        ax.set_title("Line Plot of Selected Streams")
        ax.set_xlabel("Time")
        ax.set_ylabel("Normalized Values")
        ax.legend()
        fig.tight_layout()  # Adjust layout to prevent overlap
        plt.show()

    # Create a box plot for the selected streams (ignores time intervals)
    elif plot_type == "box":
        fig, ax = plt.subplots(figsize=(8, 5))  # Create figure and axis
        df[streams].plot(kind='box', ax=ax)    # Plot directly on the defined axis
        ax.set_title("Box Plot of Selected Streams")
        ax.set_ylabel("Normalized Value")
        ax.grid(True)
        plt.show()

    # Handle invalid plot type selection
    else:
        print("Unsupported plot type selected.")
