import numpy as np
from scipy.optimize import minimize
import scipy.stats as stats
import pandas as pd

df = pd.read_csv('weatherHistory.csv')
print(df.head())
