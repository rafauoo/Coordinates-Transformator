from hirvonen import hirvonen
import numpy as np
from datetime import datetime
from neu import neu
from system_2000 import system_2000
from statistics import median, mean, variance, stdev
from io_data import write_to_txt


class Program:
    def __init__(self, coordinates, header) -> None:
        """
        creates instance of program
        Instance of program controls action of the whole program.
        It was created to separate UI in main from deep logic.
        """
        self._coordinates = coordinates
        self._curve_coords = self.curvilinear()
        self._topo_coords = self.topocentric()
        self._flat_coords = self.flat()
        self._header = header

    def coordinates(self):
        """
        returns coordinates stored in numpy array with columns:
        [SoD, X, Y, Z, Q]
        """
        return self._coordinates

    def topo_coords(self):
        """
        returns topocentric coordinates (after transformation)
        stored in numpy array with columns:
        [E, N, U]
        """
        return self._topo_coords

    def flat_coords(self):
        """
        returns flat system 2000 coordinates (after transformation)
        stored in numpy array with columns:
        [X, Y, h]
        """
        return self._flat_coords

    def mean(self, row: int):
        "calculates average of coordinate given by row"
        return mean(self._coordinates[:, row])

    def median(self, row: int):
        "calculates median of coordinate given by row"
        return median(self._coordinates[:, row])

    def variance(self, row: int):
        "calculates variance of coordinate given by row"
        return variance(self._coordinates[:, row])

    def deviation(self, row: int):
        "calculates standard deviation of coordinate given by row"
        return stdev(self._coordinates[:, row])

    def curvilinear(self):
        "transforms geocentric coordinates to curvilinear coordinates (Fi, Lam, H)"
        curve_coords = []
        for row in self._coordinates:
            x = row[1]
            y = row[2]
            z = row[3]
            fi2, lam, h, n = hirvonen(x, y, z)
            curve_coords.append([fi2, lam, h])
        return np.array(curve_coords)

    def topocentric(self):
        """
        Transforms geocentric coordinates to topocentric coordinates (E, N, U).
        It takes averages of (X, Y, Z) as the center of local coordinate system.
        """
        x0 = self.mean(1)
        y0 = self.mean(2)
        z0 = self.mean(3)
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
        """
        transforms geocentric coordinates to flat system 2000
        coordinates (X, Y, H)
        """
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
        "generates header for output file"
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
        "generates data for output file (below header)"
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

    def generate_names(self, curve=True, topo=True, flat=True):
        "generates names for values for output file"
        names = []
        names.append("sod")
        names.append("X")
        names.append("Y")
        names.append("Z")
        names.append("varia X")
        names.append("varia Y")
        names.append("varia Z")
        names.append("stdev X")
        names.append("stdev Y")
        names.append("stdev Z")
        if topo:
            names.append("E")
            names.append("N")
            names.append("U")
        if curve:
            names.append("fi")
            names.append("lam")
            names.append("h")
        if flat:
            names.append("X2000")
            names.append("Y2000")
            names.append("h")
        return names

    def generate_raport(self, curve=True, topo=True, flat=True):
        "generates raport and exports to txt file"
        header = self.generate_header()
        names = self.generate_names(curve, topo, flat)
        data = self.generate_data(curve, topo, flat)
        with open("./proj_1_raport.txt", "w") as handle:
            write_to_txt(handle, header, names, data)

    def regression_params(self, row):
        "calculates regression params (a, b)"
        value = self._coordinates[:, row]
        sod = self._coordinates[:, 0]
        mean_x = self.mean(0)
        mean_y = self.mean(row)
        xi_meanx = [x - mean_x for x in sod]
        xi_meanx_2 = [(x - mean_x)**2 for x in sod]
        yi_meany = [y - mean_y for y in value]
        up = []
        for index, x in enumerate(xi_meanx):
            up.append(x*yi_meany[index])
        a = sum(up)
        a /= sum(xi_meanx_2)
        b = mean_y - a * mean_x
        return a, b
