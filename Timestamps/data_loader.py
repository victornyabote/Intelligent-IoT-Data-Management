import pandas as pd
from datetime import datetime, timedelta

def load_data(csv_file="simple.csv", reference_date=datetime(2025, 1, 1)):
    """
    Loads time series data from a CSV file, converts 'time' (in seconds) to datetime,
    and returns the DataFrame along with the minimum and maximum datetime range.

    Parameters:
        csv_file (str): Path to the CSV file containing the data.
        reference_date (datetime): The starting datetime to offset the 'time' values.

    Returns:
        df (pd.DataFrame): DataFrame with an added 'datetime' column.
        min_datetime (datetime): Minimum datetime value in the dataset.
        max_datetime (datetime): Maximum datetime value in the dataset.
    """
    
    # Load the CSV into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Convert 'time' in seconds to actual datetime using reference_date
    df['datetime'] = df['time'].apply(lambda x: reference_date + timedelta(seconds=x))

    # Find the earliest and latest timestamps in the dataset
    min_datetime = df['datetime'].min()
    max_datetime = df['datetime'].max()

    # Return the processed DataFrame and the time range
    return df, min_datetime, max_datetime
