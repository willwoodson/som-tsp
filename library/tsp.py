import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl


class Tsp(object):
    def __init__(self, tsp_dir):
        self.tsp_dir = tsp_dir
        self.tsp_name = self.tsp_dir.split("/")[-1][:-4]

    def read_tsp(self):
        with open(self.tsp_dir) as f:
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

            print("读取到 {} 个城市。".format(dimension))

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

            file_dir = "data/cities/" + self.tsp_name + ".csv"
            cities.to_csv(file_dir)
            self.cities_original = cities
            return cities

    def normalize(self):
        """
        返回给定点向量的规范化版本

        对于给定的n维数组，通过删除初始偏移并按比例间隔对点进行归一化来标准化每个维度：
        x，y坐标归一到[0,1]后，乘以比例系数以保持x，y坐标的原始比例。
        """
        points = self.cities_original[["x", "y"]]
        ratio = 1, (points.y.max() - points.y.min()) / (points.x.max() - points.x.min())
        ratio = np.array(ratio) / max(ratio)
        norm = points.apply(lambda p: (p - p.min()) / (p.max() - p.min()))  # 默认以列为单位生成
        norm = norm.apply(lambda p: ratio * p, axis=1)  # 以行为单位生成
        self.cities_normalized = norm
        return norm

    def select_city(self):
        """选择一个随机的城市(规范化后的)。"""
        cities = self.cities_normalized
        city = cities.sample(1)[["x", "y"]].values
        return city

    def route_distance(self, route_idx):
        """返回以一定顺序遍历城市路线的总距离。"""
        cities = self.cities_original.copy()
        cities = cities.reindex(route_idx)
        points = cities[["x", "y"]]
        points_next = np.roll(points, 1, axis=0)  # 向下垂直滚动1
        distances = np.linalg.norm(points - points_next, axis=1)
        distance = np.sum(distances)
        distance = round(distance, 2)
        print("找到路线的长度为：{}".format(distance))
        self.distance = distance
        return distance

    def plot_route(self, route_idx):
        """绘制获得路线的图形表示"""
        mpl.rcParams["agg.path.chunksize"] = 10000  # 数据量很大，防止崩溃
        fig = plt.figure(figsize=(5, 5), frameon=False)
        axis = fig.add_axes([0, 0, 1, 1])
        axis.set_aspect("equal", adjustable="datalim")
        plt.axis("off")

        cities = self.cities_normalized
        route = cities.reindex(route_idx)
        route.loc[route.shape[0]] = route.iloc[0]  # 末尾添首项，组成闭环
        axis.scatter(cities["x"], cities["y"], color="red", s=4)
        axis.plot(route["x"], route["y"], color="purple", linewidth=1)

        fig_dir = "data/routes/" + self.tsp_name + "-" + str(self.distance) + ".png"
        plt.savefig(fig_dir, bbox_inches="tight", pad_inches=0, dpi=200)
        plt.close()
