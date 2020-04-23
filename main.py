from sys import argv
import numpy as np
import pandas as pd
import time

from library.som_tsp import SomTsp


if len(argv) != 2:
    print("Correct use: python src/main.py <filename>.tsp")
    exit(0)

t0 = time.time()
SomTsp = SomTsp(tsp_dir=argv[1])
SomTsp.operate()
time_cost = round(time.time() - t0, 2)
print("耗时：{} 秒".format(time_cost))
