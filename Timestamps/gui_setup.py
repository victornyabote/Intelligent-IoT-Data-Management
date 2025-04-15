import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

def setup_gui(min_datetime, max_datetime, process_callback):
    """
    Builds the GUI for selecting a time range (including seconds), stream options,
    plot type, and interval, dynamically constraining the hour, minute, and second
    selections based on the available data range.
    
    Parameters:
        min_datetime (datetime): Earliest available timestamp in the data.
        max_datetime (datetime): Latest available timestamp in the data.
        process_callback (function): Callback to execute when 'Display' is clicked.
    
    Returns:
        root (tk.Tk): The root Tkinter window object.
    """
    root = tk.Tk()
    root.title("Time & Stream Selector + Normalization")
    root.geometry("600x350")
    root.configure(bg="#f9f9f9")

    # Style settings
    style = ttk.Style()
    style.configure("TLabel", font=("Segoe UI", 10, "bold"), background="#f9f9f9")
    style.configure("TButton", font=("Segoe UI", 10))
    style.configure("TCheckbutton", font=("Segoe UI", 10), background="#f9f9f9")

    # Helper functions for computing dynamic options
    def get_allowed_hours(selected_date, for_start=True):
        # When the data spans a single day, restrict both lower and upper hours.
        if selected_date == min_datetime.date() and selected_date == max_datetime.date():
            return [f"{i:02d}" for i in range(min_datetime.hour, max_datetime.hour + 1)]
        elif for_start and selected_date == min_datetime.date():
            return [f"{i:02d}" for i in range(min_datetime.hour, 24)]
        elif (not for_start) and selected_date == max_datetime.date():
            return [f"{i:02d}" for i in range(0, max_datetime.hour + 1)]
        else:
            return [f"{i:02d}" for i in range(0, 24)]

    def get_allowed_minutes(selected_date, selected_hour, for_start=True):
        selected_hour = int(selected_hour)
        if selected_date == min_datetime.date() and selected_date == max_datetime.date():
            # When the dataset is a single day with both boundaries
            if selected_hour == min_datetime.hour and selected_hour == max_datetime.hour:
                return [f"{i:02d}" for i in range(min_datetime.minute, max_datetime.minute + 1)]
            elif selected_hour == min_datetime.hour:
                return [f"{i:02d}" for i in range(min_datetime.minute, 60)]
            elif selected_hour == max_datetime.hour:
                return [f"{i:02d}" for i in range(0, max_datetime.minute + 1)]
            else:
                return [f"{i:02d}" for i in range(0, 60)]
        elif selected_date == min_datetime.date() and for_start and selected_hour == min_datetime.hour:
            return [f"{i:02d}" for i in range(min_datetime.minute, 60)]
        elif (not for_start) and selected_date == max_datetime.date() and selected_hour == max_datetime.hour:
            return [f"{i:02d}" for i in range(0, max_datetime.minute + 1)]
        else:
            return [f"{i:02d}" for i in range(0, 60)]

    def get_allowed_seconds(selected_date, selected_hour, selected_minute, for_start=True):
        selected_hour = int(selected_hour)
        selected_minute = int(selected_minute)
        if selected_date == min_datetime.date() and selected_date == max_datetime.date():
            if (selected_hour == min_datetime.hour and selected_minute == min_datetime.minute and
                selected_hour == max_datetime.hour and selected_minute == max_datetime.minute):
                return [f"{i:02d}" for i in range(min_datetime.second, max_datetime.second + 1)]
            elif selected_hour == min_datetime.hour and selected_minute == min_datetime.minute:
                return [f"{i:02d}" for i in range(min_datetime.second, 60)]
            elif selected_hour == max_datetime.hour and selected_minute == max_datetime.minute:
                return [f"{i:02d}" for i in range(0, max_datetime.second + 1)]
            else:
                return [f"{i:02d}" for i in range(0, 60)]
        elif selected_date == min_datetime.date() and for_start and selected_hour == min_datetime.hour and selected_minute == min_datetime.minute:
            return [f"{i:02d}" for i in range(min_datetime.second, 60)]
        elif (not for_start) and selected_date == max_datetime.date() and selected_hour == max_datetime.hour and selected_minute == max_datetime.minute:
            return [f"{i:02d}" for i in range(0, max_datetime.second + 1)]
        else:
            return [f"{i:02d}" for i in range(0, 60)]

    # Update functions for start time selections
    def update_start_hour_options(event=None):
        selected_date = start_date_entry.get_date()
        hours = get_allowed_hours(selected_date, for_start=True)
        start_hour_box['values'] = hours
        if start_hour_box.get() not in hours:
            start_hour_box.set(hours[0])
        update_start_minute_options()

    def update_start_minute_options(event=None):
        selected_date = start_date_entry.get_date()
        selected_hour = start_hour_box.get() or f"{min_datetime.hour:02d}"
        minutes = get_allowed_minutes(selected_date, selected_hour, for_start=True)
        start_minute_box['values'] = minutes
        if start_minute_box.get() not in minutes:
            start_minute_box.set(minutes[0])
        update_start_second_options()

    def update_start_second_options(event=None):
        selected_date = start_date_entry.get_date()
        selected_hour = start_hour_box.get() or f"{min_datetime.hour:02d}"
        selected_minute = start_minute_box.get() or f"{min_datetime.minute:02d}"
        seconds = get_allowed_seconds(selected_date, selected_hour, selected_minute, for_start=True)
        start_second_box['values'] = seconds
        if start_second_box.get() not in seconds:
            start_second_box.set(seconds[0])

    # Update functions for end time selections
    def update_end_hour_options(event=None):
        selected_date = end_date_entry.get_date()
        hours = get_allowed_hours(selected_date, for_start=False)
        end_hour_box['values'] = hours
        if end_hour_box.get() not in hours:
            end_hour_box.set(hours[-1])
        update_end_minute_options()

    def update_end_minute_options(event=None):
        selected_date = end_date_entry.get_date()
        selected_hour = end_hour_box.get() or f"{max_datetime.hour:02d}"
        minutes = get_allowed_minutes(selected_date, selected_hour, for_start=False)
        end_minute_box['values'] = minutes
        if end_minute_box.get() not in minutes:
            end_minute_box.set(minutes[-1])
        update_end_second_options()

    def update_end_second_options(event=None):
        selected_date = end_date_entry.get_date()
        selected_hour = end_hour_box.get() or f"{max_datetime.hour:02d}"
        selected_minute = end_minute_box.get() or f"{max_datetime.minute:02d}"
        seconds = get_allowed_seconds(selected_date, selected_hour, selected_minute, for_start=False)
        end_second_box['values'] = seconds
        if end_second_box.get() not in seconds:
            end_second_box.set(seconds[-1])

    # START DATE & TIME
    ttk.Label(root, text="Start Date:").grid(row=0, column=0, padx=10, pady=10)
    start_date_entry = DateEntry(root, date_pattern='y-mm-dd',
                                 mindate=min_datetime.date(), maxdate=max_datetime.date())
    start_date_entry.set_date(min_datetime.date())
    start_date_entry.grid(row=0, column=1)
    start_date_entry.bind("<<DateEntrySelected>>", update_start_hour_options)

    ttk.Label(root, text="Start Time:").grid(row=0, column=2, padx=5)
    start_hour_box = ttk.Combobox(root, width=3)
    start_hour_box['values'] = get_allowed_hours(start_date_entry.get_date(), for_start=True)
    start_hour_box.set(f"{min_datetime.hour:02d}")
    start_hour_box.grid(row=0, column=3, padx=5)
    start_hour_box.bind("<<ComboboxSelected>>", update_start_minute_options)

    start_minute_box = ttk.Combobox(root, width=3)
    start_minute_box['values'] = get_allowed_minutes(start_date_entry.get_date(), start_hour_box.get(), for_start=True)
    start_minute_box.set(f"{min_datetime.minute:02d}")
    start_minute_box.grid(row=0, column=4, padx=5)
    start_minute_box.bind("<<ComboboxSelected>>", update_start_second_options)

    start_second_box = ttk.Combobox(root, width=3)
    start_second_box['values'] = get_allowed_seconds(start_date_entry.get_date(), start_hour_box.get(), start_minute_box.get(), for_start=True)
    start_second_box.set(f"{min_datetime.second:02d}")
    start_second_box.grid(row=0, column=5, padx=5)

    # END DATE & TIME
    ttk.Label(root, text="End Date:").grid(row=1, column=0, padx=10, pady=10)
    end_date_entry = DateEntry(root, date_pattern='y-mm-dd',
                               mindate=min_datetime.date(), maxdate=max_datetime.date())
    end_date_entry.set_date(max_datetime.date())
    end_date_entry.grid(row=1, column=1)
    end_date_entry.bind("<<DateEntrySelected>>", update_end_hour_options)

    ttk.Label(root, text="End Time:").grid(row=1, column=2, padx=5)
    end_hour_box = ttk.Combobox(root, width=3)
    end_hour_box['values'] = get_allowed_hours(end_date_entry.get_date(), for_start=False)
    end_hour_box.set(f"{max_datetime.hour:02d}")
    end_hour_box.grid(row=1, column=3, padx=5)
    end_hour_box.bind("<<ComboboxSelected>>", update_end_minute_options)

    end_minute_box = ttk.Combobox(root, width=3)
    end_minute_box['values'] = get_allowed_minutes(end_date_entry.get_date(), end_hour_box.get(), for_start=False)
    end_minute_box.set(f"{max_datetime.minute:02d}")
    end_minute_box.grid(row=1, column=4, padx=5)
    end_minute_box.bind("<<ComboboxSelected>>", update_end_second_options)

    end_second_box = ttk.Combobox(root, width=3)
    end_second_box['values'] = get_allowed_seconds(end_date_entry.get_date(), end_hour_box.get(), end_minute_box.get(), for_start=False)
    end_second_box.set(f"{max_datetime.second:02d}")
    end_second_box.grid(row=1, column=5, padx=5)

    # STREAM SELECTION
    ttk.Label(root, text="Select Streams:").grid(row=2, column=0, padx=10, pady=10)
    var_s1 = tk.BooleanVar(value=True)
    var_s2 = tk.BooleanVar(value=True)
    var_s3 = tk.BooleanVar(value=True)

    cb1 = ttk.Checkbutton(root, text="s1", variable=var_s1)
    cb2 = ttk.Checkbutton(root, text="s2", variable=var_s2)
    cb3 = ttk.Checkbutton(root, text="s3", variable=var_s3)
    cb1.grid(row=2, column=1, sticky="w")
    cb2.grid(row=2, column=2, sticky="w")
    cb3.grid(row=2, column=3, sticky="w")

    # PLOT TYPE SELECTION
    ttk.Label(root, text="Select Plot Type:").grid(row=3, column=0, padx=10, pady=10)
    plot_type = tk.StringVar(value="line")  # Default selection

    ttk.Radiobutton(root, text="Line Plot", variable=plot_type, value="line").grid(row=3, column=1, sticky="w")
    ttk.Radiobutton(root, text="Box Plot", variable=plot_type, value="box").grid(row=3, column=2, sticky="w")

    # TIME INTERVAL SELECTION
    ttk.Label(root, text="Time Interval:").grid(row=4, column=0, padx=10, pady=10)
    interval_var = tk.StringVar(value="1s")  # Default interval is 1 second
    interval_menu = ttk.Combobox(root, textvariable=interval_var,
                                 values=["1s", "1min", "5min", "15min"], width=6)
    interval_menu.grid(row=4, column=1)

    # DISPLAY BUTTON
    def on_click():
        # Trigger the callback with the updated dynamic time widgets
        process_callback(start_date_entry, start_hour_box, start_minute_box, start_second_box,
                         end_date_entry, end_hour_box, end_minute_box, end_second_box,
                         var_s1, var_s2, var_s3, plot_type, interval_var)

    ttk.Button(root, text="Display", command=on_click).grid(row=5, columnspan=6, pady=20)

    return root
