import numpy as np

from distance import select_closest


def generate_network(size):
    """
    生成给定大小的神经元网络。

    返回取值区间为[0,1]的二维点的向量。
    """
    network = np.random.rand(size, 2)
    return network


def get_neighborhood(center, radix, domain):
    """获取围绕中心索引的给定基数的高斯函数。"""

    # 在基数上施加上限以防止崩溃
    if radix < 1:
        radix = 1

    # 计算各神经元到中心的圆形网络距离
    deltas = np.absolute(center - np.arange(domain))  # 距离中心（距离城市最近的神经元）索引差值的绝对值
    distances = np.minimum(deltas, domain - deltas)  # 一维距离转换为圆形网络距离

    # 计算给定中心周围的高斯分布
    gaussian = np.exp(-(distances * distances) / (2 * (radix * radix)))
    return gaussian


def get_route(cities, network):
    """Return the route computed by a network."""
    cities["winner"] = cities[["x", "y"]].apply(
        lambda c: select_closest(network, c), axis=1, raw=True
    )

    return cities.sort_values("winner").index
