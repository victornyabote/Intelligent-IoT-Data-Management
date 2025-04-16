import pandas as pd
import numpy as np
from get_rolling_window_corr import get_rolling_window_corr

# Create a sample DataFrame to simulate the `simple` dataset or use the simple.csv or complex.csv
data = {
    'time': np.arange(0, 100),  # Simulated time column
    's1': np.random.rand(100),  # Random values for s1
    's2': np.random.rand(100),  # Random values for s2
    's3': np.random.rand(100),  # Random values for s3
}
simple = pd.DataFrame(data)

# Call the function with the sample data
window_size = 15
fig = get_rolling_window_corr(simple, window_size)