import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation


class Som(object):
    def __init__(self, cities_normalized, neuton_ratio=8, learning_rate=0.3):
        self.cities_normalized = cities_normalized
        self.neuton_num = cities_normalized.shape[0] * neuton_ratio
        self.radix = self.neuton_num // 10
        self.radix_limit = neuton_ratio / 4
        self.learning_rate = learning_rate

    def generate_network(self):
        """
        生成给定大小的神经元网络。

        返回取值区间为[0,1]的二维点的向量。
        """
        self.neurons = np.random.rand(self.neuton_num, 2)
        neurons = self.neurons.copy()
        neurons = np.row_stack((neurons, neurons[0]))  # 末尾添首项，组成闭环
        self.neurons_list = neurons
        print("创建拥有 {} 个神经元的神经网络。".format(self.neuton_num))

    def select_closest(self, city):
        """返回与当前城市最近的神经元位置索引。"""

        # 矩阵每个行向量求向量的2范数（欧式距离）
        distances = np.linalg.norm(self.neurons - city, axis=1)
        self.winner_idx = distances.argmin()
        return self.winner_idx

    def get_neighborhood(self):
        """计算获胜神经元周围的高斯分布"""

        # 防止神经元基数衰减到0,出现数学错误
        if self.radix < 1:
            self.radix = 1

        # 计算各神经元到获胜神经元的圆形网络距离
        # 各神经元到获胜神经元的单向距离（索引差值的绝对值）
        deltas = np.absolute(self.winner_idx - np.arange(self.neuton_num))
        # 单向距离转换为圆形网络距离
        distances = np.minimum(deltas, self.neuton_num - deltas)

        # 计算获胜神经元周围的高斯分布
        gaussian = np.exp(-(distances ** 2) / (2 * (self.radix ** 2)))
        self.gaussian = gaussian[:, np.newaxis]  # 转换成2维

    def update_weights(self, city):
        """
        更新网络的权重
        
        使得获胜神经元的优胜邻域内神经元像城市靠近
        """

        self.neurons += self.gaussian * self.learning_rate * (city - self.neurons)

    def updae_rates(self):
        """衰减学习率 & 减少神经元基数（增强局部搜索能力）"""

        self.learning_rate = self.learning_rate * 0.99997
        self.radix = self.radix * 0.9997

    def plot_network(self):
        """绘制问题的图形表示"""
        mpl.rcParams["agg.path.chunksize"] = 10000  # 数据量很大，防止崩溃
        fig = plt.figure(figsize=(5, 5), frameon=False)
        axis = fig.add_axes([0, 0, 1, 1])
        axis.set_aspect("equal", adjustable="datalim")
        plt.axis("off")

        cities = self.cities_normalized.copy()
        neurons = self.neurons.copy()
        neurons = np.row_stack((neurons, neurons[0]))  # 末尾添首项，组成闭环
        self.neurons_list = np.row_stack((self.neurons_list, neurons))
        axis.scatter(cities["x"], cities["y"], color="red", s=5)
        axis.plot(
            neurons[:, 0], neurons[:, 1], "r.", ls="-", color="#0063ba", markersize=2
        )
        plt.savefig("data/som.png", bbox_inches="tight", pad_inches=0, dpi=200)
        plt.close()

    def check(self, i):
        complete = 0
        if self.radix < self.radix_limit:
            print("-------------------------------------------")
            print("半径已完全衰减，总迭代次数为：{}".format(i),)
            complete = 1
        if self.learning_rate < 0.001:
            print("-------------------------------------------")
            print("学习率已完全降低，总迭代次数为：{}".format(i),)
            complete = 1
        return complete

    def get_route(self):
        """返回由网络计算的路径。"""
        cities = self.cities_normalized.copy()
        cities["winner_idx"] = cities[["x", "y"]].apply(
            lambda c: self.select_closest(c), axis=1, raw=True
        )
        route_idx = cities.sort_values("winner_idx").index

        return route_idx

    def ani_network(self):
        mpl.rcParams["agg.path.chunksize"] = 10000  # 数据量很大，防止崩溃
        fig = plt.figure(figsize=(5, 5), frameon=False)
        axis = fig.add_axes([0, 0, 1, 1])
        axis.set_aspect("equal", adjustable="datalim")
        plt.axis("off")
        ims = []

        cities = self.cities_normalized.copy()
        for i in range(self.neurons_list.shape[0] // (self.neuton_num + 1)):
            if i > 2:
                j = i * (self.neuton_num + 1)
                neurons = self.neurons_list[j : j + self.neuton_num + 1]
                flame = []
                flame += axis.scatter(
                    cities["x"], cities["y"], color="red", s=3
                ).findobj()
                flame += axis.plot(
                    neurons[:, 0],
                    neurons[:, 1],
                    "r.",
                    ls="-",
                    color="#0063ba",
                    markersize=2,
                )
                ims.append(flame)

        for i in range(20):
            neurons = self.neurons_list[j : j + self.neuton_num + 1]
            flame = []
            flame += axis.scatter(cities["x"], cities["y"], color="red", s=3).findobj()
            flame += axis.plot(
                neurons[:, 0],
                neurons[:, 1],
                "r.",
                ls="-",
                color="#0063ba",
                markersize=1,
            )
            ims.append(flame)

        ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=2000)
        ani.save("data/som.gif", writer="pillow")
        plt.close()
