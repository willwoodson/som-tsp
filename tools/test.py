import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time


cities = pd.read_csv("data/optimal.csv")
print(cities)
a = int(cities[cities["tsp"] == "st70"]["optimal_solution"])
print(a)
