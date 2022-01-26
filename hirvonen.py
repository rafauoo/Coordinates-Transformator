import math
import numpy as np


def hirvonen(x, y, z):
    a = 6378137
    e2 = 0.00669438002290
    eps1 = 0.000001  # sekundy
    eps = eps1/3600 * math.pi/180  # rad
    # 1
    # r=[(x**2+y**2)]**(1/2)
    r = math.sqrt(x**2 + y**2)

    # 2
    fi = math.atan(z / (r * (1 - e2)))  # radiany
    fi2 = 2*fi
    while np.abs(fi2 - fi) > eps:
        fi = fi2

    # 3
        N = a/math.sqrt(1 - e2 * math.sin(fi2)**2)

    # 4
        h = (r / np.cos(fi) - N)

    # 5
        fi2 = math.atan(z/(r*(1 - e2 * (N/(N+h)))))  # radiany

    # 6
    N = a/np.sqrt(1-e2*np.sin(fi2)**2)
    h = r/math.cos(fi) - N
    lam = math.atan(y/x)
    return fi2, lam, h, N


def st_m_s(fi):
    fi = fi * 180 / math.pi
    degrees = np.floor(fi)
    minutes = np.floor((fi - degrees)*60)
    seconds = ((fi - degrees - minutes / 60) * 3600)
    return degrees, minutes, seconds
