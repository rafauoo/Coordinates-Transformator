import hirvonen
import numpy as np


class Program:
    def __init__(self, coordinates, header) -> None:
        self._coordinates = coordinates
        self._curve_coords = self.curvilinear()
        self._topo_coords = self.topocentric()
        self._flat_coords = self.flat()
        self._header = header

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
            fi2, lam, h, n = hirvonen.hirvonen(x, y, z)
            curve_coords.append(fi2, lam, h)
        return np.array(curve_coords)

    def topocentric(self):
        pass
    
    def flat(self):
        pass
