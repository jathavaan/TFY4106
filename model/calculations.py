import numpy as np

M = 31  # g
r = 11  # mm
g = 9.81  # m/s^2
c = 2 / 5


# Funksjon 1
def speed_y(y_0, y_1):
    global g
    global c
    return np.sqrt((2 * g * (y_0 - y_1)) / (1 + c))


# Funksjon 2
def speed_x(y_0, y_1):
    global g
    global c
    return np.sqrt((2 * g * (y_0 - y_1)) / (1 + c))


# Funksjon 3
def curvature(d1y, d2y):
    return d2y / (1 + d1y ** 2) ** 3 / 2


# Funksjon 4
def centripetal_acceleration(v, k):
    return v ** 2 * k


# Funksjon 7
def normal_force(beta, y_0, y_1, yd1, yd2):
    global M
    global g

    v = speed_x(y_0, y_1)
    k = curvature(yd1, yd2)

    a = centripetal_acceleration(v, k)
    return M * (g * np.cos(beta) + a)


# Funksjon 16
def acceleration(beta):
    global g
    return - (5 * g * np.sin(beta)) / 7


# Funksjon 17
def friction(beta):
    global M
    global g
    return (2 * M * g * np.sin(beta)) / 7


