import numpy as np


def select_closest(network, city):
    """返回与当前城市最近的神经元位置索引。"""

    # 矩阵每个行向量求向量的2范数（欧式距离）
    distances = np.linalg.norm(network - city, axis=1)
    closest = distances.argmin()
    return closest


def route_distance(cities):
    """返回以一定顺序遍历城市路线的总距离。"""
    points = cities[["x", "y"]]
    points_next = np.roll(points, 1, axis=0)  # 向下垂直滚动1
    distances = np.linalg.norm(points - points_next, axis=1)
    distance = np.sum(distances)
    return distance
