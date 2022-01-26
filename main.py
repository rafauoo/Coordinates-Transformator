from io_data import import_from_txt
from program import Program


def main():
    with open("./proj_1_dane-2.txt") as handle:
        coordinates, header = import_from_txt(handle)
    program = Program(coordinates, header)
    print(program._flat_coords)
    curve = input("Transform coordinates to curvilinear(Fi, Lam, H)? (YES or NO): ")
    curve = True if curve == "YES" else False
    topo = input("Transform coordinates to topocentric(E, N, U)? (YES or NO): ")
    topo = True if topo == "YES" else False
    flat = input("Transform coordinates to system 2000(Fi, lam, H)? (YES or NO): ")
    flat = True if flat == "YES" else False
    program.generate_raport(curve, topo, flat)


if __name__ == "__main__":
    main()
