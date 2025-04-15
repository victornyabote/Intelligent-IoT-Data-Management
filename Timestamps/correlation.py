def calculate_pairwise_correlation(df):
    """
    Calculates and prints pairwise Pearson correlations between selected numeric streams.

    Parameters:
        df (pd.DataFrame): Normalized dataframe with 'datetime' and stream columns.
    """
    stream_cols = df.columns.drop('datetime')

    if len(stream_cols) < 2:
        print("Not enough streams selected to compute correlation.")
        return

    print("\nPairwise Correlations (Selected Time Window):")
    for i in range(len(stream_cols)):
        for j in range(i + 1, len(stream_cols)):
            col1, col2 = stream_cols[i], stream_cols[j]
            corr = df[col1].corr(df[col2])
            print(f"Correlation between {col1.strip()} and {col2.strip()}: {corr:.4f}")
