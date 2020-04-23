import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

if __name__ == "__main__":
    # fig = plt.figure()
    # ims = []
    # for i in range(1, 10):
    #     im = plt.plot(np.linspace(0, i, 10), np.linspace(0, np.random.randint(i), 10))
    #     ims.append(im)
    # ani = animation.ArtistAnimation(fig, ims, interval=200, repeat_delay=1000)
    # ani.save("test.gif", writer="pillow")

    fig = plt.figure(figsize=(5, 5), frameon=False)
    axis = fig.add_axes([0, 0, 1, 1])
    axis.set_aspect("equal", adjustable="datalim")
    plt.axis("off")
    ims = []

    for i in range(1, 10):
        axis.scatter(
            np.linspace(0, i, 10), np.linspace(0, i, 10), color="red", s=5
        ).findobj()
        im = axis.plot(np.linspace(0, i, 10), np.linspace(0, np.random.randint(i), 10))
        ims.append(im)
    print(ims)
    ani = animation.ArtistAnimation(fig, ims, interval=20, repeat_delay=1000)
    ani.save("test.gif", writer="pillow")
    plt.close()
