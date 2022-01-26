from hirvonen import hirvonen
import numpy as np
from datetime import datetime
from neu import neu
from system_2000 import system_2000
from statistics import median, mean, variance, stdev
from io_data import write_to_txt


class Program:
    def __init__(self, coordinates, header) -> None:
        self._coordinates = coordinates
        self._curve_coords = self.curvilinear()
        self._topo_coords = self.topocentric()
        self._flat_coords = self.flat()
        self._header = header

    def mean(self, row):
        return mean(self._coordinates[:, row])

    def median(self, row):
        return median(self._coordinates[:, row])

    def variance(self, row):
        return variance(self._coordinates[:, row])

    def deviation(self, row):
        return stdev(self._coordinates[:, row])

    def curvilinear(self):
        curve_coords = []
        for row in self._coordinates:
            x = row[1]
            y = row[2]
            z = row[3]
            fi2, lam, h, n = hirvonen(x, y, z)
            curve_coords.append([fi2, lam, h])
        return np.array(curve_coords)

    def topocentric(self):
        # liczymy srednie dla x,y,z
        x0 = self.mean(1)
        y0 = self.mean(2)
        z0 = self.mean(3)
        print(x0, y0, z0)
        topo_coords = []
        fi2, lam, h, n = hirvonen(x0, y0, z0)
        for row in self._coordinates:
            x = row[1]
            y = row[2]
            z = row[3]
            enu = neu(fi2, lam, x, y, z, x0, y0, z0)
            enu = np.transpose(enu)
            topo_coords.append([enu[0, 0], enu[0, 1], enu[0, 2]])
        return np.array(topo_coords)

    def flat(self):
        flat_coords = []
        for row in self._coordinates:
            x = row[1]
            y = row[2]
            z = row[3]
            fi2, lam, h, n = hirvonen(x, y, z)
            x0, y0 = system_2000(fi2, lam)
            flat_coords.append([x0, y0, h])
        return np.array(flat_coords)

    def generate_header(self):
        header = {}
        header["Author"] = "Imie i nazwisko"
        header["Date"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        quantity_6 = 0
        quantity_1 = 0
        for data in self._coordinates:
            if data[4] == 6:
                quantity_6 += 1
            if data[4] == 1:
                quantity_1 += 1
        header["Quantity Q=6"] = quantity_6
        header["Quantity Q=1"] = quantity_1
        header["Mean X"] = self.mean(1)
        header["Mean Y"] = self.mean(2)
        header["Mean Z"] = self.mean(3)
        header["Median X"] = self.median(1)
        header["Median Y"] = self.median(2)
        header["Median Z"] = self.median(3)
        return header

    def generate_data(self, curve=True, topo=True, flat=True):
        variance_x = self.variance(1)
        variance_y = self.variance(2)
        variance_z = self.variance(3)
        stdev_x = self.deviation(1)
        stdev_y = self.deviation(2)
        stdev_z = self.deviation(3)
        data = []
        for index, row in enumerate(self._coordinates):
            data_line = []
            data_line.append(row[0])  # sod
            data_line.append(row[1])  # X
            data_line.append(row[2])  # Y
            data_line.append(row[3])  # Z
            data_line.append(variance_x)
            data_line.append(variance_y)
            data_line.append(variance_z)
            data_line.append(stdev_x)
            data_line.append(stdev_y)
            data_line.append(stdev_z)
            if topo:
                data_line.append(self._topo_coords[index, 0])  # e
                data_line.append(self._topo_coords[index, 1])  # n
                data_line.append(self._topo_coords[index, 2])  # u
            if curve:
                data_line.append(self._curve_coords[index, 0])  # fi
                data_line.append(self._curve_coords[index, 1])  # lam
                data_line.append(self._curve_coords[index, 2])  # h
            if flat:
                data_line.append(self._flat_coords[index, 0])  # x
                data_line.append(self._flat_coords[index, 1])  # y
                data_line.append(self._flat_coords[index, 2])  # h
            data.append(data_line)
        return data

    def generate_raport(self, curve=True, topo=True, flat=True):
        header = self.generate_header()
        data = self.generate_data(curve, topo, flat)
        with open("./proj_1_raport.txt", "w") as handle:
            write_to_txt(handle, header, data)
