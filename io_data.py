import os
import numpy as np
from types import coroutine


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
                sod = float(time[0]) * 3600 + float(time[1]) * 60 + float(time[2])
                coordinates.append([sod, 
                                    float(data[2]),
                                    float(data[3]),
                                    float(data[4]),
                                    int(data[5])])
    return np.array(coordinates), header