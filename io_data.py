import numpy as np


def import_from_txt(handle):
    coordinates = []
    header = {}
    is_header = True
    for line in handle:
        if len(line) > 2:
            if line[2] == "=":
                is_header = False
            if line[0] == "%" and is_header:
                line = line.strip("%").strip()
                key = ""
                data = ""
                is_key = True
                for char in line:
                    if is_key is True:
                        key = key if char == " " else key + char
                    else:
                        data = data + char
                    if char == ":":
                        is_key = False
                header[key[:-1]] = data.strip()
            elif line[0] != "%":
                data = line.strip().split()
                time = data[1].split(":")
                sod = float(time[0]) * 3600 + float(time[1]) * 60
                sod += float(time[2])
                coordinates.append([sod,
                                    float(data[2]),
                                    float(data[3]),
                                    float(data[4]),
                                    int(data[5])])
    return np.array(coordinates), header


def write_to_txt(handle, header, names, data):
    for line in header:
        li = str(line) + ": " + str(header[line]) + "\n"
        handle.write(li)
    handle.write("=" * 300 + "\n")
    for name in names:
        handle.write(f"{name:<16}")
    handle.write("\n")
    for line in data:
        for item in line:
            handle.write(f"{round(item, 5):<12}" + "\t")
        handle.write("\n")
