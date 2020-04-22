import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


def plot_network(cities, neurons, name="diagram.png", ax=None):
    """绘制问题的图形表示"""
    mpl.rcParams["agg.path.chunksize"] = 10000  # 数据量很大，防止崩溃

    if not ax:
        fig = plt.figure(figsize=(5, 5), frameon=False)
        axis = fig.add_axes([0, 0, 1, 1])

        axis.set_aspect("equal", adjustable="datalim")
        plt.axis("off")

        axis.scatter(cities["x"], cities["y"], color="red", s=4)
        neurons = neurons.copy()
        neurons = np.row_stack((neurons, neurons[0]))  # 末尾添首项，组成闭环

        axis.plot(
            neurons[:, 0], neurons[:, 1], "r.", ls="-", color="#0063ba", markersize=2
        )

        plt.savefig("data/evolution.png", bbox_inches="tight", pad_inches=0, dpi=200)
        plt.close()

    else:
        ax.scatter(cities["x"], cities["y"], color="red", s=4)
        ax.plot(
            neurons[:, 0], neurons[:, 1], "r.", ls="-", color="#0063ba", markersize=2
        )
        return ax


def plot_route(cities, route, name="diagram.png", ax=None):
    """Plot a graphical representation of the route obtained"""
    mpl.rcParams["agg.path.chunksize"] = 10000

    if not ax:
        fig = plt.figure(figsize=(5, 5), frameon=False)
        axis = fig.add_axes([0, 0, 1, 1])

        axis.set_aspect("equal", adjustable="datalim")
        plt.axis("off")

        axis.scatter(cities["x"], cities["y"], color="red", s=4)
        route = cities.reindex(route)
        route.loc[route.shape[0]] = route.iloc[0]  # 末尾添首项，组成闭环
        axis.plot(route["x"], route["y"], color="purple", linewidth=1)

        plt.savefig(name, bbox_inches="tight", pad_inches=0, dpi=200)
        plt.close()

    else:
        ax.scatter(cities["x"], cities["y"], color="red", s=4)
        route = cities.reindex(route)
        route.loc[route.shape[0]] = route.iloc[0]
        ax.plot(route["x"], route["y"], color="purple", linewidth=1)
        return ax
