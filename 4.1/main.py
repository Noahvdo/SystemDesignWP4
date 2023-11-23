import numpy as np

import math

from determine_dimensions import calculate_max_y_transverse

from determine_mass import calculate_mass


parameters = {}


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


parameters["d1"] = [0.05, 0.17]

# parameters.append["D2", 0, 4]

# parameters.append["A2", 0, 4]

# parameters.append(["A3", 0, 4])

# parameters.append["A5", 0, 4]

parameters["t1"] = [0.0001, 0.2]

# parameters.append["t2", 0, 4]

# parameters.append["t3", 0, 4]

# parameters.append["h", 0, 4]

parameters["w"] = [0.051, 0.2]

# parameters.append["n_holes", 0, 4]


def max_min(_min, _max, value):
    max(_min, min(_max, value))


iterations = 100


for key, value in parameters.items():
    parameters[key].append(value[0])


def gen():
    highestFunctionOutput = 0
    lowestMass = 99999999
    highestParams = {}
    for k in range(iterations ** len(parameters)):
        loopedParameters = []

        for i, (key, value) in enumerate(parameters.items()):
            value[2] = value[0] + math.floor(
                k % (iterations ** (i + 1)) / iterations**i
            ) * (value[1] - value[0]) / (iterations - 1)

        result = calculate_max_y_transverse(
            parameters["d1"][2], parameters["t1"][2], parameters["w"][2]
        )
        mass = calculate_mass(
            parameters["d1"][2], parameters["t1"][2], parameters["w"][2]
        )
        # if highestFunctionOutput < result:
        if result > 1.2 * 1220 and mass < lowestMass:
            highestFunctionOutput = result
            lowestMass = mass
            for key, value in parameters.items():
                highestParams[key] = parameters[key][2]

    for key, value in highestParams.items():
        print(f"{key}: {value}")
    print(f"Mass: {lowestMass}")
    print(f"Force: {highestFunctionOutput}")


gen()
