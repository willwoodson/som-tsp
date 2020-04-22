from sys import argv
import numpy as np
import pandas as pd
import time

from initialize import read_tsp, normalize
from neuron import generate_network, get_neighborhood, get_route
from distance import select_closest, route_distance
from plot import plot_network, plot_route


def main():
    # if len(argv) != 2:
    #     print("请正确使用格式: python src/main.py <filename>.tsp")
    #     return -1

    # cities = read_tsp(argv[1])

    cities = read_tsp("assets/st70.tsp")
    # cities = read_tsp("assets/t10.tsp")

    route = som(cities, 100000)

    cities = cities.reindex(route)

    distance = route_distance(cities)

    print("找到路线的长度为：{}".format(distance))


def som(cities, iterations, learning_rate=0.3):
    """
    使用自组织映射解决旅行商问题
    """
    # 获得标准化的城市集 (w/ coord in [0,1])
    cities = cities.copy()  # 复制一份用于标准化，不修改原始数据
    cities[["x", "y"]] = normalize(cities[["x", "y"]])

    # 神经元数设置为城市数的8倍
    n = cities.shape[0] * 8

    # 生成合适的神经元网络：
    network = generate_network(n)
    print("创建拥有 {} 个神经元的神经网络。开始迭代：".format(n))

    for i in range(iterations):
        if not i % 100:
            print("\t> 迭代次数： {}/{}".format(i, iterations), end="\r")

        # 选择一个随机的城市
        city = cities.sample(1)[["x", "y"]].values
        winner_idx = select_closest(network, city)

        # 生成将更改应用于获胜者 的 高斯函数过滤器
        gaussian = get_neighborhood(winner_idx, n // 10, network.shape[0])  # 整数除法

        # 更新网络的权重（使得获胜神经元的优胜邻域内神经元像城市靠近）
        network += gaussian[:, np.newaxis] * learning_rate * (city - network)

        # 衰减学习率 & 减少神经元数（增强局部搜索能力）
        learning_rate = learning_rate * 0.99997
        n = n * 0.9997

        # 绘图间隔
        if not i % 1000:
            plot_network(cities, network, name="diagrams/{:05d}.png".format(i))

        # 检查是否有任何参数完全衰减。
        if n < 1:
            print("-------------------------------------------")
            print("半径已完全衰减，总迭代次数为： {} ".format(i),)
            break
        if learning_rate < 0.001:
            print("-------------------------------------------")
            print("学习率已完全降低，总迭代次数为： {} ".format(i),)
            break
    else:
        print("-------------------------------------------")
        print("总迭代次数为 {} .".format(iterations))

    plot_network(cities, network, name="diagrams/final.png")

    route = get_route(cities, network)
    plot_route(cities, route, "diagrams/route.png")
    return route


if __name__ == "__main__":
    t = time.time()
    main()
    print("耗时： {} .".format(time.time() - t))
