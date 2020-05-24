import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation


class Som(object):
    def __init__(self):
        pass

    def initialize(self, cities_normalized, neuron_ratio=8, learning_rate=0.3):
        self.cities_normalized = cities_normalized
        self.neuron_num = cities_normalized.shape[0] * neuron_ratio
        self.neuron_num = (self.neuron_num // 4) * 4
        self.radix = self.neuron_num / 10
        self.radix_limit = neuron_ratio / 10
        self.learning_rate = learning_rate

        # 方案二
        self.radix_0 = self.radix
        self.learning_rate_0 = self.learning_rate
        self.t1 = 3000
        self.t2 = 30000

        self.t3 = 3000

    def generate_network(self):
        """
        生成给定大小的神经元网络。

        返回取值区间为[0,1]的二维点的向量。
        """

        # 随机生成神经元
        # self.neurons = np.random.rand(self.neuron_num, 2)

        # 初始神经元拓扑结构为围绕城市的矩形
        a = self.cities_normalized

        x_min, x_max, y_min, y_max = (
            a["x"].min(),
            a["x"].max(),
            a["y"].min(),
            a["y"].max(),
        )

        # 初始门限半径
        self.radius_0 = np.sqrt((x_max - x_min) ** 2 + (y_max - y_min) ** 2) / 4
        # print(self.radius_0)
        self.radius = 0.00001

        neurons = np.ones((self.neuron_num, 2))
        a = int(self.neuron_num / 4)
        neurons[0:a, 0] = np.linspace(x_min, x_max, a)
        neurons[0:a, 1] = y_min
        neurons[a : 2 * a, 0] = x_max
        neurons[a : 2 * a, 1] = np.linspace(y_min, y_max, a)
        neurons[2 * a : 3 * a, 0] = np.linspace(x_max, x_min, a)
        neurons[2 * a : 3 * a, 1] = y_max
        neurons[3 * a : 4 * a, 0] = x_min
        neurons[3 * a : 4 * a, 1] = np.linspace(y_max, y_min, a)
        self.neurons = neurons

        neurons = neurons.copy()
        neurons = np.row_stack((neurons, neurons[0]))  # 末尾添首项，组成闭环
        self.neurons_list = neurons
        print("创建拥有 {} 个神经元的神经网络。".format(self.neuron_num))

    def select_closest(self, city):
        """返回与当前城市最近的神经元位置索引。"""

        # 矩阵每个行向量求向量的2范数（欧式距离）
        distances = np.linalg.norm(self.neurons - city, axis=1)
        self.winner_idx = distances.argmin()

        # 计算orc系数
        distence = distances.min()
        self.orc = np.exp((-(distence ** 2) / (2 * self.radius ** 2)) + 0.5)
        # if (1 - self.orc) < 0.01 and self.orc < 1:
        #     print(self.orc)

        return self.winner_idx

    def get_neighborhood(self):
        """计算获胜神经元周围的高斯分布"""

        # 防止神经元基数衰减到0,出现数学错误
        if self.radix < 0.001:
            self.radix = 0.001

        # 计算各神经元到获胜神经元的圆形网络距离
        # 各神经元到获胜神经元的单向距离（索引差值的绝对值）
        deltas = np.absolute(self.winner_idx - np.arange(self.neuron_num))
        # 单向距离转换为圆形网络距离
        distances = np.minimum(deltas, self.neuron_num - deltas)

        # 计算获胜神经元周围的高斯分布
        gaussian = np.exp(-(distances ** 2) / (2 * (self.radix ** 2)))
        self.gaussian = gaussian[:, np.newaxis]  # 转换成2维

    def update_weights(self, city):
        """
        更新网络的权重
        
        使得获胜神经元的优胜邻域内神经元像城市靠近
        """
        self.neurons += (
            self.orc * self.gaussian * self.learning_rate * (city - self.neurons)
        )

        # self.neurons += self.gaussian * self.learning_rate * (city - self.neurons)

    def updae_rates(self, i):
        """衰减学习率 & 减少神经元基数（增强局部搜索能力）"""

        # 方案一
        self.radix = self.radix * 0.9997
        self.learning_rate = self.learning_rate * 0.99997

        # 方案二
        # self.radix = self.radix_0 * np.exp(-i / self.t1)
        # self.learning_rate = self.learning_rate_0 * np.exp(-i / self.t2)

        self.radius = self.radius_0 * (1 - np.exp((-i - 1) / self.t3))

    def plot_network(self, name):
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
        plt.savefig(name, bbox_inches="tight", pad_inches=0, dpi=200)
        plt.savefig("data/som.png", bbox_inches="tight", pad_inches=0, dpi=200)
        plt.close()

    def check(self, i):
        complete = 0
        if self.radix < self.radix_limit:
            print("-------------------------------------------")
            print("半径已完全衰减，总迭代次数为：{}".format(i),)
            complete = 1
        if self.learning_rate < 0.01:
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

    def ani_network(self, name):
        mpl.rcParams["agg.path.chunksize"] = 10000  # 数据量很大，防止崩溃
        fig = plt.figure(figsize=(5, 5), frameon=False)
        axis = fig.add_axes([0, 0, 1, 1])
        axis.set_aspect("equal", adjustable="datalim")
        plt.axis("off")
        ims = []

        cities = self.cities_normalized.copy()
        for i in range(self.neurons_list.shape[0] // (self.neuron_num + 1)):
            if i > 2:
                j = i * (self.neuron_num + 1)
                neurons = self.neurons_list[j : j + self.neuron_num + 1]
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
            neurons = self.neurons_list[j : j + self.neuron_num + 1]
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
        ani.save(name, writer="pillow")
        plt.close()
