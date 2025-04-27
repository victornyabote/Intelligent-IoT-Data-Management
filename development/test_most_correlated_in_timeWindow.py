# test get_most_correlated using complex.csv
import pandas as pd
import numpy as np
from most_correlated_in_timeWindow import most_correlated_in_timeWindow

# get `complex.csv` dataset
complex = np.genfromtxt('complex.csv', delimiter=',', names=True, encoding= 'utf-8-sig')



# Call the function with the sample data
most_correlated_in_selected_window = most_correlated_in_timeWindow(complex, 150, 400)

