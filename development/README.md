# 1 get_rolling_window_corr.py is a first step to analysing time-series data

## This function cCalculates rolling correlation between two columns of a pandas df that has 3 columns with 'time' column as index. 

    Each number in 'time' represents 10 minutes interval using simple and complex datasets.

    window_size is the number of rows to look back. ie. we are calculating the correlation of the previous 15 rows (150 minutes) of the two columns. 

    ie. the correlation showing at 'time = 15' is the correlation of the values at 'time = 0' to 'time = 14' (15 rows) of the two columns.

    The correlation from 'time = 0' till 'time = 14' is NaN because there are not enough rows to calculate the correlation. 

    Parameters:
    df (pd.DataFrame): The DataFrame containing only 3 streams the data.
    
    Returns:
    pd.Series: A Series containing the rolling correlation values.

# 2 most_correlated_streams_window.py
## This function finds most correlated two streams within the defined time-window. 

    Each number in 'time' represents 10 minutes interval using simple and complex datasets. Other datasets may have different time intervals.

    `window_start` is the start row number of the selected window to compare, `window_end` is the ending row number of the window ie. we are calculating the correlation between s1 and s2, s1 and s3, s2 and s3. 
    
    Returns:
    the two most correlated streams and their correlation value

# 3 IoT_wire.png is a wireframe to include these two functions and more visualisation on a dashboard with time-series data.

## License

[MIT](https://choosealicense.com/licenses/mit/)