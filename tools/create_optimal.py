import pandas as pd
import numpy as np


filename = "tools/最优解.txt"
with open(filename) as f:
    cities = pd.read_csv(
        f,
        sep=" : ",  # 指定分隔符
        names=["tsp", "optimal_solution"],  # 列名,数据类型
        dtype={"tsp": str, "optimal_solution": np.float64},
        engine="python",
    )
    cities.to_csv("tools/optimal.csv")
