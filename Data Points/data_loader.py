import pandas as pd
import numpy as np

def load_data(csv_file):
    """
    Loads time series data from a CSV file, assumes the first column contains 
    date/time or sequential information, replaces it with numeric indices, 
    and returns the processed DataFrame along with the index range and time column name.
    
    Parameters:
        csv_file (str): Path to the CSV file.

    Returns:
        df (pd.DataFrame): DataFrame with 'data_point' as the time/index column.
        min_dp (int): Minimum value of the data point index.
        max_dp (int): Maximum value of the data point index.
        time_col (str): Name of the new time/index column ('data_point').
    """
    # Read CSV into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Store the original time column name (assumed to be the first column)
    original_time_col = df.columns[0]
    
    # Rename that column to "data_point" for consistency
    df.rename(columns={original_time_col: "data_point"}, inplace=True)
    
    # Replace its values with sequential integers (0, 1, 2, ...)
    df["data_point"] = list(range(len(df)))
    
    # Get the min and max index values
    min_dp = df["data_point"].min()
    max_dp = df["data_point"].max()
    
    # Return the modified DataFrame and useful metadata
    return df, min_dp, max_dp, "data_point"
