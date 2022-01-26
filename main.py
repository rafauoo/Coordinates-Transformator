from io_data import import_from_txt
from program import Program


def main():
    with open("./test.txt") as handle:
        coordinates, header = import_from_txt(handle)
    program = Program(coordinates, header)
    print(program._flat_coords)
    program.generate_raport()


if __name__ == "__main__":
    main()