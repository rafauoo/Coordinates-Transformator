from matplotlib import pyplot as plt
import numpy as np


def geocentric_plot_linear(program):
    "creates linear plot for geocentric coordinates (X, Y, Z)"
    x = program.coordinates()[:, 1]
    y = program.coordinates()[:, 2]
    z = program.coordinates()[:, 3]
    sod = program.coordinates()[:, 0]
    fig, axs = plt.subplots(3, constrained_layout=True)
    axs[0].plot(sod, x)
    axs[0].set_title("X", fontsize=20)
    axs[0].set_xlabel("Second Of The Day", fontsize=8)
    axs[0].set_ylabel("X")
    axs[0].yaxis.major.formatter._useMathText = True
    axs[1].plot(sod, y)
    axs[1].set_title("Y", fontsize=20)
    axs[1].set_xlabel("Second Of The Day", fontsize=8)
    axs[1].set_ylabel("Y")
    axs[1].yaxis.major.formatter._useMathText = True
    axs[2].plot(sod, z)
    axs[2].set_title("Z", fontsize=20)
    axs[2].set_xlabel("Second Of The Day", fontsize=8)
    axs[2].set_ylabel("Z")
    axs[2].yaxis.major.formatter._useMathText = True
    plt.gcf().set_size_inches(14, 10)
    plt.savefig("geocentric_linear_plot.png")
    plt.show()


def geocentric_plot_histogram(program):
    "creates histogram plot for geocentric coordinates (X, Y, Z)"
    x = program.coordinates()[:, 1]
    y = program.coordinates()[:, 2]
    z = program.coordinates()[:, 3]
    fig, axs = plt.subplots(3, constrained_layout=True)
    axs[0].hist(x, histtype=u'step')
    axs[0].set_title("X", fontsize=20)
    axs[0].set_xlabel("X", fontsize=8)
    axs[0].set_ylabel("Count")
    axs[0].xaxis.major.formatter._useMathText = True
    axs[1].hist(y, histtype=u'step')
    axs[1].set_title("Y", fontsize=20)
    axs[1].set_xlabel("Y", fontsize=8)
    axs[1].set_ylabel("Count")
    axs[1].xaxis.major.formatter._useMathText = True
    axs[2].hist(z, histtype=u'step')
    axs[2].set_title("Z", fontsize=20)
    axs[2].set_xlabel("Z", fontsize=8)
    axs[2].set_ylabel("Count")
    axs[2].xaxis.major.formatter._useMathText = True
    plt.gcf().set_size_inches(14, 10)
    plt.savefig("geocentric_histogram_plot.png")
    plt.show()


def enu_scatter_plot(program):
    "creates scatter plot for topocentric coordinates (E, N, U)"
    e = program.topo_coords()[:, 0]
    n = program.topo_coords()[:, 1]
    u = program.topo_coords()[:, 2]
    sod = program.coordinates()[:, 0]
    fig, (ax1, ax2) = plt.subplots(1, 2, constrained_layout=True)
    ax1.scatter(e, n)
    ax1.legend(["Points (E,N)"])
    ax1.set_title("E, N", fontsize=20)
    ax1.set_xlabel("E", fontsize=8)
    ax1.set_ylabel("N")
    ax2.scatter(sod, u)
    ax2.set_title("U", fontsize=20)
    ax2.set_xlabel("Second Of The Day", fontsize=8)
    ax2.set_ylabel("U")
    ax2.legend(["U"])
    plt.gcf().set_size_inches(14, 10)
    plt.savefig("topocentric_scatter_plot.png")
    plt.show()


def system2000_scatter_plot(program):
    "creates scatter plot for flat system 2000 coordinates (X, Y, h)"
    x = program.flat_coords()[:, 0]
    y = program.flat_coords()[:, 1]
    h = program.flat_coords()[:, 2]
    sod = program.coordinates()[:, 0]
    fig, (ax1, ax2) = plt.subplots(1, 2, constrained_layout=True)
    ax1.scatter(x, y)
    ax1.legend(["Points (X, Y)"])
    ax1.set_title("X, Y", fontsize=20)
    ax1.set_xlabel("X", fontsize=8)
    ax1.set_ylabel("Y")
    ax1.yaxis.major.formatter._useMathText = True
    ax1.xaxis.major.formatter._useMathText = True
    ax2.scatter(sod, h)
    ax2.set_title("h", fontsize=20)
    ax2.set_xlabel("Second Of The Day", fontsize=8)
    ax2.set_ylabel("h")
    ax2.legend(["H"])
    plt.gcf().set_size_inches(14, 10)
    plt.savefig("flat_system_2000_scatter_plot.png")
    plt.show()


def regression_plot(program, a, b, what_coord):
    """"
    Creates linear plot for given param (X, Y or Z) with regression line
    and error plot.
    """
    sod = program.coordinates()[:, 0]
    row = -1
    if what_coord == "X":
        row = 1
    if what_coord == "Y":
        row = 2
    if what_coord == "Z":
        row = 3
    all_x_np = np.arange(int(min(sod)), int(max(sod)), 1)
    all_x = [x for x in all_x_np]
    all_y = [a * x + b for x in all_x]
    sod = program.coordinates()[:, 0]
    fig, axs = plt.subplots(2, constrained_layout=True)
    # Regression plot
    axs[0].plot(sod, program.coordinates()[:, row])
    axs[0].plot(all_x, all_y)
    axs[0].set_title(f"{what_coord} & Regression Line", fontsize=20)
    axs[0].legend([f"{what_coord}", "Regression Line"])
    axs[0].set_xlabel("Second Of The Day", fontsize=8)
    axs[0].set_ylabel(f"{what_coord}")
    axs[0].yaxis.major.formatter._useMathText = True
    axs[0].xaxis.major.formatter._useMathText = True
    # Error plot
    axs[1].plot(sod, program.coordinates()[:, row])
    axs[1].plot(all_x, all_y)
    axs[1].set_title(f"{what_coord} & Regression Line", fontsize=20)
    axs[1].legend([f"{what_coord}", "Regression Line"])
    axs[1].set_xlabel("Second Of The Day", fontsize=8)
    axs[1].set_ylabel(f"{what_coord}")
    axs[1].yaxis.major.formatter._useMathText = True
    axs[1].xaxis.major.formatter._useMathText = True
    plt.gcf().set_size_inches(14, 10)
    plt.savefig(f"regression_plot_for_{what_coord}.png")
    plt.show()
