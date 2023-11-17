import numpy as np
import math

print("hallo")
print("hoi")

parameters = []

# Load forces
loads = {"x": 0, "y": 0, "z": 0}
# Moment forces
moments = {"x": 0, "y": 0, "z": 0}

# time
t = 0
# change in time step dt
dt = 0.01

#
# Dimensions of the lug
# ["name", min, max]

parameters.append["D1", 0, 4]
parameters.append["D2", 0, 4]
parameters.append["A2", 0, 4]
parameters.append["A3", 0, 4]
parameters.append["A5", 0, 4]
parameters.append["t1", 0, 4]
parameters.append["t2", 0, 4]
parameters.append["t3", 0, 4]
parameters.append["h", 0, 4]
parameters.append["w", 0, 4]
parameters.append["n_holes", 0, 4]


# A_br = t_1 * D1


def max_min(_min, _max, value):
    max(_min, min(_max, value))


# Constant K for yielding
def calculate_K_ty(x_value):
    x_value = max(0, min(1.4, x_value))
    y = (
        -0.0046429324
        + 1.24667 * x_value
        + 0.2731277 * (x_value**2)
        - 0.769549 * (x_value**3)
        + 0.292853 * (x_value**4)
    )
    return y


# K_ty = calculate_K_ty(A_br / A_av)


# Force P for yielding
# P_ty = K_ty * A_br * F_ty


# A1 ->  t1  ->  t2  ->  t3  ->  D1  ->  D2
iterations = 5
# parameter.append[1, 0, 0, 4, ""]
# parameters = [[1, 0, 0, 4], [2, 0, 0, 4], [3, 0, 0, 4]]

pars = len(parameters)
for i in range(pars):
    parameters[i][4] = i + 1
    parameters[i][3] = parameters[i][1]


def iterate():
    # 0 = name  1 = min  2 = max  3 = value  4 = index
    getal = 1
    while getal < iterations**pars:
        for par in parameters:
            i = par[4] - 1
            if i <= pars:
                if math.floor(getal / (iterations**i)) == math.ceil(
                    getal / (iterations) ** i
                ):
                    par[3] = par[3] + (par[2] - par[1]) / (iterations - 1)
                    for _par in parameters:
                        l = _par[4] - 1
                        if l + 1 < i + 1:
                            _par[3] = _par[1]
        getal = getal + 1
        list = []
        for r in parameters:
            list.append([r[0], r[3]])
        print(list)
