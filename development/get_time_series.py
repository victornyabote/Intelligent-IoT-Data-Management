import pandas as pd
import os

def get_time_series(dataset_name, start_idx=0, end_idx=None, output_prefix=None):
    """
    Load and preprocess time-series IoT sensor data from a CSV file.

    Args:
        dataset_name (str): Path to the CSV dataset (e.g., "datasets/complex.csv").
        start_idx (int): Starting row index for slicing.
        end_idx (int, optional): Ending row index for slicing (exclusive). Defaults to None (until end).
        output_prefix (str, optional): Prefix for exported CSV/JSON files. If None, uses dataset name.

    Returns:
        pd.DataFrame: Cleaned and sliced DataFrame containing only numeric sensor columns.

    Raises:
        FileNotFoundError: If the dataset file does not exist.
        ValueError: If start_idx or end_idx are out of bounds.
    """
    
    # Validate file exists
    if not os.path.isfile(dataset_name):
        raise FileNotFoundError(f"Dataset '{dataset_name}' not found.")
    
    # Load dataset
    df = pd.read_csv(dataset_name)
    
    # Keep only numeric columns (e.g., sensor readings)
    numeric_df = df.select_dtypes(include='number')
    
    # Validate indices
    if start_idx < 0 or (end_idx is not None and end_idx > len(numeric_df)):
        raise ValueError("Invalid start or end index range.")
    
    # Slice data
    sliced_df = numeric_df.iloc[start_idx:end_idx]
    
    # Prepare output file prefix
    if output_prefix is None:
        output_prefix = os.path.splitext(os.path.basename(dataset_name))[0] + "_slice"
    
    # Export to CSV and JSON
    sliced_df.to_csv(f"{output_prefix}.csv", index=False)
    sliced_df.to_json(f"{output_prefix}.json", orient='records')
    
    print(f"Exported: {output_prefix}.csv and {output_prefix}.json")
    
    return sliced_df

# Example usage:
if __name__ == "__main__":
    df_slice = get_time_series("datasets/complex.csv", start_idx=250, end_idx=500)
    print(df_slice.head())