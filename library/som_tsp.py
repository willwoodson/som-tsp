import numpy as np
import pandas as pd
import time

from library.tsp import Tsp
from library.som import Som


class SomTsp(object):
    def __init__(self, tsp_dir, neuton_ratio=8, iterations=100000, learning_rate=0.3):
        self.tsp_dir = tsp_dir
        self.neuton_ratio = neuton_ratio
        self.iterations = iterations
        self.learning_rate = learning_rate

    def operate(self):
        self.initialize()
        self.train()
        self.analyze()

    def initialize(self):
        self.Tsp = Tsp(self.tsp_dir)
        self.cities_original = self.Tsp.read_tsp()
        self.cities_normalized = self.Tsp.normalize()

        self.Som = Som(self.cities_normalized, self.neuton_ratio, self.learning_rate,)
        self.Som.generate_network()

    def train(self):
        for i in range(self.iterations):
            if not i % 100:
                print("\t> 迭代次数： {}/{}".format(i, self.iterations), end="\r")

            city = self.Tsp.select_city()  # 选择一个随机的城市
            self.Som.select_closest(city)  # 获胜神经元序号
            self.Som.get_neighborhood()  # 生成优胜邻域的高斯函数过滤器
            self.Som.update_weights(city)  # 更新网络的权重
            self.Som.updae_rates()  # 衰减学习率 & 减少神经元基数

            # 绘制神经元轨迹
            if not i % 1000:
                self.Som.plot_network()

            # 检查是否有任何参数完全衰减。
            complete = self.Som.check(i)
            if complete:
                break
        else:
            print("-------------------------------------------")
            print("总迭代次数为：{}.".format(self.iterations))

    def analyze(self):
        # self.Som.ani_network()  # Som网络动画。
        route_idx = self.Som.get_route()  # Som网络计算的路径。
        distence = self.Tsp.route_distance(route_idx)  # 路径长度
        self.Tsp.plot_route(route_idx)  # 绘制路径轨迹
