# this is particular written for simple and complex dataset
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_rolling_window_corr(data, window_size):
    """
    Calculate rolling correlation between two columns in a a pandas df that has 3 columns with 'time' column as index. 

    Each number in 'time' represents 10 minutes interval using simple and complex datasets.

    window_size is the number of rows to look back. ie. we are calculating the correlation of the previous 15 rows (150 minutes) of the two columns. 

    ie. the correlation showing at 'time = 15' is the correlation of the values at 'time = 0' to 'time = 14' (15 rows) of the two columns.

    The correlation from 'time = 0' till 'time = 14' is NaN because there are not enough rows to calculate the correlation. 

    Parameters:
    df (pd.DataFrame): The DataFrame containing only 3 streams the data.
    
    Returns:
    pd.Series: A Series containing the rolling correlation values.
    """
    
    df = pd.DataFrame(data, columns=['time', 's1', 's2', 's3'])
    df.set_index('time', inplace=True)

    # window_size = 15 # 150 mins, 10-mins intervals

    # rolling correlation 
    df['corr_s1_s2'] = df['s1'].rolling(window=window_size, closed="left").corr(df['s2'])

    df['corr_s1_s3'] = df['s1'].rolling(window=window_size, closed="left").corr(df['s3'])

    df['corr_s2_s3'] = df['s2'].rolling(window=window_size, closed="left").corr(df['s3'])

    #print(df.head(20))
    # save the rolling correlation to a CSV file
    df.to_csv('rolling_corr.csv', index=True)
    # save the rolling correlation to a JSON file
    # convert the DataFrame to JSON format
    df.to_json('rolling_corr.json', orient='records', lines=True)
    # plot the rolling correlation
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df['corr_s1_s2'], label='s1 and s2', color='green', marker='o', linestyle='dashed', linewidth=2, markersize=6, markevery=50)
    ax.plot(df['corr_s2_s3'], label='s2 and s3', color='black', marker='o', linestyle='dashed', linewidth=2, markersize=6, markevery=30)
    ax.plot(df['corr_s1_s3'], label='s1 and s3', color='red', linestyle='dashed', linewidth=2)
   
    ax.set_title('Rolling Correlation')
    ax.set_xlabel('Time')
    ax.set_ylabel('Correlation')
    ax.legend()
    ax.grid()
    fig.tight_layout()
    # Save the figure
    fig.savefig('rolling_corr.png')
    plt.show()
    plt.close(fig)
    return fig