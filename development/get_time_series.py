# development/get_time_series.py

import pandas as pd
import os

def get_time_series(dataset_path, start_idx=0, end_idx=None, output_prefix=None):
    """
    Load and preprocess IoT sensor dataset from CSV using row-idx slicing.

    Args:
        dataset_path (str): Path to the CSV dataset.
        start_idx (int): Starting row index (inclusive).
        end_idx (int, optional): Ending row index (exclusive). Defaults to EOF.
        output_prefix (str, optional): Prefix for output files. Defaults to dataset base name.

    Returns:
        pd.DataFrame: Numeric-only slice of data.

    Raises:
        FileNotFoundError: When dataset_path does not exist.
        ValueError: If indices are invalid.
    """
    if not os.path.isfile(dataset_path):
        raise FileNotFoundError(f"Dataset '{dataset_path}' not found.")

    df = pd.read_csv(dataset_path)
    numeric_df = df.select_dtypes(include='number')

    total_rows = len(numeric_df)
    end_idx = end_idx or total_rows

    if start_idx < 0 or end_idx > total_rows or end_idx <= start_idx:
        raise ValueError("Invalid start_idx or end_idx.")

    sliced_df = numeric_df.iloc[start_idx:end_idx]

    if output_prefix is None:
        base = os.path.splitext(os.path.basename(dataset_path))[0]
        output_prefix = f"{base}_slice"

    sliced_df.to_csv(f"{output_prefix}.csv", index=False)
    sliced_df.to_json(f"{output_prefix}.json", orient='records')
    print(f"Exported '{output_prefix}.csv' and '{output_prefix}.json'.")

    return sliced_df


if __name__ == "__main__":
    # Example run: adjust path and indices as needed
    df = get_time_series("datasets/complex.csv", start_idx=250, end_idx=500)
    print(df.head())
