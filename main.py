from io_data import import_from_txt
from program import Program


def main():
    with open("./proj_1_dane-2.txt") as handle:
        coordinates, header = import_from_txt(handle)
    Program(coordinates, header)


if __name__ == "__main__":
    main()