from sys import argv
import numpy as np
import pandas as pd
import time

# from library.som.som_tsp import SomTsp

# from library.orc_som.som_tsp import SomTsp

from library.orcts_som.som_tsp import SomTsp


def initialize(step_num):
    df = pd.read_csv("data/optimal.csv", index_col=0)
    step_list = []
    for i in range(step_num):
        step = "step" + str(i + 1)
        step_list.append(step)
        df[step] = 0
    df["average"] = 0
    df["deviation"] = 0

    df.to_csv("data/record.csv")
    return step_list


def record(i, tsp_name, distence):
    df = pd.read_csv("data/record.csv", index_col=0)
    step = "step" + str(i + 1)
    a = df[df.tsp == tsp_name].index
    df.loc[a, step] = distence
    df.to_csv("data/record.csv")


def compare(step_list):
    df = pd.read_csv("data/record.csv", index_col=0)
    distences = df[step_list]
    df["average"] = distences.mean(axis=1)
    df["deviation"] = (df["average"] - df["optimal_solution"]) / df["optimal_solution"]
    df["deviation"] = df.apply(
        lambda x: str(round(x["deviation"] * 100, 2)) + "%", axis=1
    )
    print(df)
    df.to_csv("data/record.csv")


t0 = time.time()
step_num = 5
tsp_name = ["st70", "pr76", "rat99", "ch130", "kroA200"]
SomTsp = SomTsp()
step_list = initialize(step_num)

for i in range(step_num):
    for j in range(5):
        t1 = time.time()
        print("-------------------" + tsp_name[j] + "--------------------")
        SomTsp.operate(
            "assets/" + tsp_name[j] + ".tsp", neuton_ratio=8, learning_rate=0.3
        )
        record(i, SomTsp.tsp_name, SomTsp.distence)
        time_cost = round(time.time() - t1, 2)
        print("耗时：{} 秒".format(time_cost))
        print("  ")

compare(step_list)
time_cost = round((time.time() - t0), 2)
minute = int(time_cost // 60)
second = int(time_cost - (60 * minute))
print("总耗时：{} 分 {} 秒".format(minute, second))
