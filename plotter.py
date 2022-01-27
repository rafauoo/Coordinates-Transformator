from matplotlib import pyplot as plt


def geocentric_plot_linear(program):
    x = program.coordinates()[:, 1]
    y = program.coordinates()[:, 2]
    z = program.coordinates()[:, 3]
    sod = program.coordinates()[:, 0]
    fig, axs = plt.subplots(3)
    axs[0].plot(sod, x)
    axs[0].set_title("X")
    axs[1].plot(sod, y)
    axs[1].set_title("Y")
    axs[2].plot(sod, z)
    axs[2].set_title("Z")
    plt.savefig("geocentric_linear_plot.png")
    plt.show()


def geocentric_plot_histogram(program):
    x = program.coordinates()[:, 1]
    y = program.coordinates()[:, 2]
    z = program.coordinates()[:, 3]
    fig, axs = plt.subplots(3)
    axs[0].hist(x)
    axs[0].set_title("X")
    axs[1].hist(y)
    axs[1].set_title("Y")
    axs[2].hist(z)
    axs[2].set_title("Z")
    plt.savefig("geocentric_histogram_plot.png")
    plt.show()


def enu_scatter_plot(program):
    e = program.topo_coords()[:, 0]
    n = program.topo_coords()[:, 1]
    u = program.topo_coords()[:, 2]
    sod = program.coordinates()[:, 0]
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.scatter(sod, e)
    ax1.scatter(sod, n)
    ax1.legend(["E", "N"])
    ax1.set_title("E, N")
    ax2.scatter(sod, u)
    ax2.set_title("U")
    ax2.legend(["U"])
    plt.savefig("topocentric_scatter_plot.png")
    plt.show()


def system2000_scatter_plot(program):
    x = program.flat_coords()[:, 0]
    y = program.flat_coords()[:, 1]
    h = program.flat_coords()[:, 2]
    sod = program.coordinates()[:, 0]
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.scatter(sod, x)
    ax1.scatter(sod, y)
    ax1.legend(["X", "Y"])
    ax1.set_title("X, Y")
    ax2.scatter(sod, h)
    ax2.set_title("H")
    ax2.legend(["H"])
    plt.savefig("flat_system_2000_scatter_plot.png")
    plt.show()