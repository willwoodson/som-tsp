import pandas as pd
import numpy as np


def read_tsp(filename):
    """
    读取.tsp文件中的二维城市坐标到pandas DataFrame中
    """
    with open(filename) as f:
        # 读取整个文件所有行，保存在一个列表(list)变量中
        lines = f.readlines()
        dimension, node_coord_start, i = 0, 0, 0

        # 读取tsp问题城市维度，二维城市坐标起始位
        while not node_coord_start:
            line = lines[i]
            if line.startswith("DIMENSION :"):
                dimension = int(line.split(" ")[-1])
            if line.startswith("NODE_COORD_SECTION"):
                node_coord_start = i + 1
            i = i + 1

        print("Problem with {} cities read.".format(dimension))

        # 读取二维城市坐标
        f.seek(0)  # 从文件头开始读取
        cities = pd.read_csv(
            f,
            skiprows=node_coord_start,  # 需要忽略的行数（从文件开始处算起）
            sep=" ",  # 指定分隔符
            names=["city", "x", "y"],  # 列名,数据类型
            dtype={"city": str, "x": np.float64, "y": np.float64},
            header=None,  # 指定行数用来作为列名，已经设定列名，置None
            nrows=dimension,  # 需要读取的行数
        )
        cities.to_csv("data/cities.csv")

        return cities


def normalize(points):
    """
    返回给定点向量的规范化版本

    对于给定的n维数组，通过删除初始偏移并按比例间隔对点进行归一化来标准化每个维度：
    x，y坐标归一到[0,1]后，乘以比例系数以保持x，y坐标的原始比例。
    """
    ratio = 1, (points.y.max() - points.y.min()) / (points.x.max() - points.x.min())
    ratio = np.array(ratio) / max(ratio)
    norm = points.apply(lambda p: (p - p.min()) / (p.max() - p.min()))  # 默认以列为单位生成
    norm = norm.apply(lambda p: ratio * p, axis=1)  # 以行为单位生成
    return norm
