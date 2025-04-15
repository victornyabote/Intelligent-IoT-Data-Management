def calculate_pairwise_correlation(df, time_col="data_point"):
    """
    Calculates and prints pairwise Pearson correlations between sensor streams.

    Parameters:
        df (pd.DataFrame): DataFrame containing the time column and sensor data.
        time_col (str): Name of the time/index column (default is 'data_point').
    """
    # Get the list of columns excluding the time/index column
    stream_cols = df.columns.drop(time_col)

    # Check if there are at least two streams to compute correlation
    if len(stream_cols) < 2:
        print("Not enough streams selected to compute correlation.")
        return

    # Print header for correlation output
    print("\nPairwise Correlations (Selected Data Points):")

    # Loop through each unique pair of streams
    for i in range(len(stream_cols)):
        for j in range(i + 1, len(stream_cols)):
            col1, col2 = stream_cols[i], stream_cols[j]
            
            # Compute Pearson correlation between the two streams
            corr = df[col1].corr(df[col2])
            
            # Print the result, removing extra spaces from column names
            print(f"Correlation between {col1.strip()} and {col2.strip()}: {corr:.4f}")
