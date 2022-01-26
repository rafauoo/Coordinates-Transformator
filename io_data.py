import os
import numpy as np
from types import coroutine


def import_from_txt(handle):
    coordinates = []
    header = {}
    for line in handle:
        if line[0] == "%" and line[2] != "=":
            line = line.strip("%")
            data = line.strip().split()
            data.pop(0)
            data.pop(0)
            str_data = ""
            for str in data:
                str_data += str + " "
            header[data[0]] = str_data
        elif not line[2] == "=":
            data = line.strip().split()
            time = data[1].split(":")
            sod = float(time[0]) * 3600 + float(time[1]) * 60 + float(time[2])
            coordinates.append([sod, 
                                float(data[2]),
                                float(data[3]),
                                float(data[4]),
                                int(data[5])])
    return np.array(coordinates), header