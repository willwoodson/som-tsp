from sys import argv
import numpy as np
import pandas as pd
import time

from library.som.som_tsp import SomTsp


t0 = time.time()

# 命令行模式
# if len(argv) != 2:
#     print("Correct use: python src/main.py <filename>.tsp")
#     exit(0)
# SomTsp = SomTsp(tsp_dir=argv[1], learning_rate=0.3)

# 直接运行模式
tsp_name = ["st70", "pr76", "rat99", "ch130", "kroA200"]
SomTsp = SomTsp("assets/" + tsp_name[3] + ".tsp", learning_rate=0.3)

SomTsp.operate()
time_cost = round(time.time() - t0, 2)
print("耗时：{} 秒".format(time_cost))
