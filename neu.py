import numpy as np


def neu(F1, L1, x, y, z, x0, y0, z0):
    R = np.array([[-np.sin(L1), -np.sin(F1) * np.cos(L1), np.cos(F1) * np.cos(L1)],
                 [np.cos(L1), -np.sin(F1) * np.sin(L1), np.cos(F1) * np.sin(L1)],
                 [0, np.cos(F1), np.sin(F1)]])
    Rt = np.transpose(R)
    xt = x - x0
    yt = y - y0
    zt = z - z0
    xyzt = np.array([[xt], [yt], [zt]])
    enu = Rt.dot(xyzt)
    return enu
