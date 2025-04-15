import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

def setup_gui(min_dp, max_dp, sensor_columns, process_callback):
    """
    Sets up the Tkinter GUI for selecting data point range, sensor streams, and plot type.

    Parameters:
        min_dp (int): Minimum value of the data point index.
        max_dp (int): Maximum value of the data point index.
        sensor_columns (list): List of available sensor stream column names.
        process_callback (function): Function to call when the Display button is clicked.

    Returns:
        root (tk.Tk): The root window of the Tkinter interface.
    """
    # Create the main window
    root = tk.Tk()
    root.title("Data Point & Stream Selector + Normalization")
    root.geometry("500x300")
    root.configure(bg="#f9f9f9")

    # Define UI style for consistency
    style = ttk.Style()
    style.configure("TLabel", font=("Segoe UI", 10, "bold"), background="#f9f9f9")
    style.configure("TButton", font=("Segoe UI", 10))
    style.configure("TCheckbutton", font=("Segoe UI", 10), background="#f9f9f9")

    # Start Data Point input
    ttk.Label(root, text="Start Data Point:").grid(row=0, column=0, padx=10, pady=10)
    start_spinbox = ttk.Spinbox(root, from_=min_dp, to=max_dp, width=10)
    start_spinbox.set(min_dp)
    start_spinbox.grid(row=0, column=1)

    # End Data Point input
    ttk.Label(root, text="End Data Point:").grid(row=1, column=0, padx=10, pady=10)
    end_spinbox = ttk.Spinbox(root, from_=min_dp, to=max_dp, width=10)
    end_spinbox.set(max_dp)
    end_spinbox.grid(row=1, column=1)

    # Sensor Stream selection (dynamic checkboxes based on sensor columns)
    ttk.Label(root, text="Select Streams:").grid(row=2, column=0, padx=10, pady=10)
    stream_vars = {}
    for idx, stream in enumerate(sensor_columns):
        var = tk.BooleanVar(value=True)  # default selection is True
        chk = ttk.Checkbutton(root, text=stream, variable=var)
        chk.grid(row=2 + idx // 3, column=1 + idx % 3, sticky="w", padx=5)
        stream_vars[stream] = var  # store the variable for each stream

    # Plot type selection (line or box)
    ttk.Label(root, text="Select Plot Type:").grid(row=5, column=0, padx=10, pady=10)
    plot_type = tk.StringVar(value="line")  # default is line plot
    ttk.Radiobutton(root, text="Line Plot", variable=plot_type, value="line").grid(row=5, column=1, sticky="w")
    ttk.Radiobutton(root, text="Box Plot", variable=plot_type, value="box").grid(row=5, column=2, sticky="w")

    # Define what happens when the user clicks the Display button
    def on_click():
        process_callback(start_spinbox, end_spinbox, stream_vars, plot_type)

    # Display button to trigger the callback
    ttk.Button(root, text="Display", command=on_click).grid(row=6, columnspan=4, pady=20)

    # Return the configured root window
    return root
