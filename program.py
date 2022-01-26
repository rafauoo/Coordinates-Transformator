from hirvonen import hirvonen
import numpy as np
from datetime import datetime
from neu import neu
from system_2000 import system_2000


class Program:
    def __init__(self, coordinates, header) -> None:
        self._coordinates = coordinates
        self._curve_coords = self.curvilinear()
        self._topo_coords = self.topocentric()
        self._flat_coords = self.flat()
        self._header = header

    def mean(self, row):
        return sum(self._coordinates[:, row]) / len(self._coordinates[:, row])

    def coordinates(self):
        return self._coordinates

    def header(self):
        return self._header

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
            flat_coords.append([x0, y0])
        return np.array(flat_coords)

    def generate_raport(self):
        header = {}
        header["Autor"] = "Imie i nazwisko"
        header["Data"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        quantity_6 = 0
        quantity_1 = 0
        for data in self._coordinates:
            print(data)
            if data[4] == 6:
                quantity_6 += 1
            if data[4] == 1:
                quantity_1 += 1
        header["Ilosc Q=6:"] = quantity_6
        header["Ilosc Q=1:"] = quantity_1
        print(header)
