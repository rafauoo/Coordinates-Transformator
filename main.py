from io_data import import_from_txt
from program import Program
from plotter import geocentric_plot_linear, geocentric_plot_histogram
from plotter import enu_scatter_plot, system2000_scatter_plot
from plotter import regression_plot


def main():
    "Console UI"
    with open("./proj_1_dane-2.txt") as handle:
        coordinates, header = import_from_txt(handle)
    program = Program(coordinates, header)
    curve = input("Transform coordinates to curvilinear(Fi, Lam, H)? (YES or NO): ")
    curve = True if curve == "YES" else False
    topo = input("Transform coordinates to topocentric(E, N, U)? (YES or NO): ")
    topo = True if topo == "YES" else False
    flat = input("Transform coordinates to system 2000(X, Y, H)? (YES or NO): ")
    flat = True if flat == "YES" else False
    program.generate_raport(curve, topo, flat)
    again = True
    while again:
        print("Plot options: ")
        print("1. Geocentric linear plot (X, Y, Z - 3 subplots)")
        print("2. Geocentric histogram plot (X, Y, Z - 3 subplots)")
        print("3. Geocentric linear plot with regression and errors for given coordinate (2 subplots)")
        print("4. Topocentric scatter plot ((E, N), Z - 2 subplots)")
        print("5. Flat system 2000 scatter plot ((X, Y), h - 2 subplots)")
        what_plot = input("Type plot number (or type anything else to exit): ")
        if what_plot == "1":
            geocentric_plot_linear(program)
        if what_plot == "2":
            geocentric_plot_histogram(program)
        if what_plot == "3":
            what_coord = input("What coordinate do you want to make plot with? (X or Y or Z): ")
            if what_coord == "X":
                a, b = program.regression_params(1)
            if what_coord == "Y":
                a, b = program.regression_params(2)
            if what_coord == "Z":
                a, b = program.regression_params(3)
            regression_plot(program, a, b, what_coord)
            program.generate_regression_raport(a, b, what_coord)
        if what_plot == "4":
            enu_scatter_plot(program)
        if what_plot == "5":
            system2000_scatter_plot(program)
        again = input("Do you want to draw another plot? (YES or NO): ")
        again = True if again == "YES" else False


if __name__ == "__main__":
    main()
