import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler

def normalize_data(df, time_col=None, reference_datetime=datetime(2025, 1, 1), interval="1s"):
    """
    Cleans and normalizes a time-series DataFrame by:
    - Handling flexible time formats
    - Resampling based on a specified interval
    - Interpolating missing values
    - Scaling numeric columns between 0 and 1 via Min-Max Scaling

    Parameters:
        df (pd.DataFrame): Input DataFrame containing a time column and sensor streams.
        time_col (str): Optional. The name of the time column. If None, the first column is assumed.
        reference_datetime (datetime): Reference timestamp for converting numeric time values.
        interval (str): Resampling frequency (e.g., '1s', '1min', '5min').

    Returns:
        pd.DataFrame: Cleaned, resampled, and normalized DataFrame with 'datetime' and sensor columns.
    """
    
    df = df.copy()

    # Drop completely empty rows and columns
    df.dropna(how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    # Identify the time column
    if time_col is None:
        time_col = df.columns[0]

    # Parse or construct datetime column from the time values
    try:
        if pd.api.types.is_numeric_dtype(df[time_col]):
            # Case 1: Numeric time (e.g., seconds since start or timestamp like 202504081430)
            if df[time_col].astype(str).str.len().max() >= 12:
                # Treat as compact datetime format like '202504081430'
                df['datetime'] = pd.to_datetime(df[time_col].astype(str), format='%Y%m%d%H%M', errors='coerce')
            else:
                # Treat as seconds since reference
                df['datetime'] = df[time_col].apply(lambda x: reference_datetime + timedelta(seconds=float(x)))
        else:
            # Case 2: Already a valid datetime string
            df['datetime'] = pd.to_datetime(df[time_col], errors='coerce', dayfirst=True)
    except Exception as e:
        raise ValueError(f"Error parsing datetime: {e}")

    # Dropp rows where datetime parsing failed
    df.dropna(subset=['datetime'], inplace=True)

    # Sort by datetime to ensure chronological order
    df.sort_values('datetime', inplace=True)

    # Resample data to uniform interval (e.g., 1s, 1min)
    df.set_index('datetime', inplace=True)
    df = df.resample(interval).mean().reset_index()

    # Identify and interpolate numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if time_col in numeric_cols:
        numeric_cols.remove(time_col)
    df[numeric_cols] = df[numeric_cols].interpolate(method='linear', limit_direction='both')

    # Normalize numeric columns to [0, 1] range using Min-Max scaling
    # scaler = MinMaxScaler()
    # df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # Drop the original time column (if different from 'datetime')
    if time_col != 'datetime' and time_col in df.columns:
        df.drop(columns=[time_col], inplace=True)

    # Return the final DataFrame with datetime and normalized values
    return df[['datetime'] + numeric_cols]
