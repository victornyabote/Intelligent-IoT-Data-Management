# this is particular written for datasets like simple and complex dataset, and will work with any dataset that has 3 streams with 'time' column as index.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def most_correlated_in_timeWindow(data, window_start, window_end):
    """
    Find most correlated two streams within the defined time-window. 

    Each number in 'time' represents 10 minutes interval using simple and complex datasets. Other datasets may have different time intervals.

    `window_start` is the start row number of the selected window to compare, `window_end` is the ending row number of the window ie. we are calculating the correlation between s1 and s2, s1 and s3, s2 and s3. 
    
    Returns:
    the two most correlated streams and their correlation value
    """
    try:
        window_start = int(window_start)
        window_end = int(window_end)
    except ValueError:
        print("Invalid input: window_start and window_end should be integers.")
        
    if window_start < 0 or window_end < 0:
        print("Invalid input: window_start and window_end should be non-negative integers.")
        return None
    
    if window_start >= window_end:
        print("Invalid input: window_start should be less than window_end.")
        return None
    
    if window_start >= len(data) or window_end > len(data):
        print("Invalid input: window_start or window_end exceeds the length of the data.")
        return None

    df = pd.DataFrame(data, columns=['time', 's1', 's2', 's3'])
    df.set_index('time', inplace=True)

    window_data = df[['s1', 's2', 's3']].iloc[window_start : window_end, :]

    most_correlated = []
    # Calculate the correlation between each pair of streams
    corr_12 = window_data['s1'].corr(window_data['s2'])
    corr_13 = window_data['s1'].corr(window_data['s3'])
    corr_23 = window_data['s2'].corr(window_data['s3'])

    if abs(corr_12) > abs(corr_13) and abs(corr_12) > abs(corr_23):
        most_correlated.append('s1')
        most_correlated.append('s2')
        highest_correlation = corr_12
    elif abs(corr_13) > abs(corr_12) and abs(corr_13) > abs(corr_23):
        most_correlated.append('s1')
        most_correlated.append('s3')
        highest_correlation = corr_13
    elif abs(corr_23) > abs(corr_12) and abs(corr_23) > abs(corr_13):
        most_correlated.append('s2')
        most_correlated.append('s3')
        highest_correlation = corr_23
    else:
        most_correlated.append('No correlation found')
        most_correlated.append(0)   

    #print(most_correlated)
    # print(f'Most correlated streams: {most_correlated[0]} and {most_correlated[1]}') 
    # print('Correlation value:', highest_correlation)
 
    df.to_csv('most_correlated_streams_window.csv', index=True)
    # Save the most correlated streams to a JSON file
    # convert the DataFrame to JSON format
    df.to_json('most_correlated_streams_window.json', orient='records', lines=True)  
 # Plot all streams and give heavier weight to the most correlated stream
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df[most_correlated[0]], label=most_correlated[0], color='green', marker='o', linestyle='dashed', linewidth=4, markersize=6, markevery=50)
    ax.plot(df[most_correlated[1]], label=most_correlated[1], color='red', marker='o', linestyle='dashed', linewidth=4, markersize=6, markevery=30)
    # get the other stream number
    other_stream = list(set(['s1', 's2', 's3']) - set(most_correlated))
    # get max y-values
    max_y = np.max(df[['s1', 's2', 's3']].max())
    #print("max:", max_y)

    ax.plot(df[other_stream], label=other_stream, color='black', linestyle='dashed', linewidth=2)

    # Highlight the selected window
    ax.axvspan(window_start, window_end, color='yellow', alpha=0.5, label='Selected Window')

    # add correlation value to the plot
    ax.text((window_end+window_start)/2, max_y-0.1,f'Correlation: {highest_correlation:.2f}', color='blue', weight='bold', size='x-large', horizontalalignment='center')

    ax.set_title('Most Correlated Streams are {} and {} (in heavy plots)'.format(most_correlated[0], most_correlated[1]), weight='bold', size='x-large')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.legend()
    ax.grid()
    fig.tight_layout()
    # Save the figure
    fig.savefig('most_correlated_streams_window.png')
    plt.show()
    plt.close(fig)
    # Save the most correlated streams to a CSV file
      
    return fig, most_correlated, highest_correlation
    
    