from sys import argv
import numpy as np
import pandas as pd
import time

# from library.som.som_tsp import SomTsp

# from library.orc_som.som_tsp import SomTsp

from library.orcts_som.som_tsp import SomTsp


# 直接运行模式
tsp_name = ["st70", "pr76", "rat99", "ch130", "kroA200"]
i = 2
SomTsp = SomTsp()

t0 = time.time()
print("-------------------" + tsp_name[i] + "--------------------")
SomTsp.operate("assets/" + tsp_name[i] + ".tsp", learning_rate=0.3)
time_cost = round(time.time() - t0, 2)
print("耗时：{} 秒".format(time_cost))
print("  ")


# 命令行模式
# if len(argv) != 2:
#     print("Correct use: python src/main.py <filename>.tsp")
#     exit(0)
# tsp_dir = argv[1]
# tsp_name = tsp_dir.split("/")[-1][:-4]
# SomTsp = SomTsp()

# t0 = time.time()
# print("-------------------" + tsp_name + "--------------------")
# SomTsp.operate(tsp_dir, learning_rate=0.3)
# time_cost = round(time.time() - t0, 2)
# print("耗时：{} 秒".format(time_cost))
# print("  ")
