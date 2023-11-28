import numpy as np
import math
from determine_dimensions import (
    calculate_max_y_transverse,
    calculate_shear_bearing_failure_axial,
)
from determine_mass import calculate_mass
import time


import os

user_input = os.environ.get("USER_INPUT", "n")

# Load forces

loads = {"x": 0, "y": 0, "z": 0}

# Moment forces

moments = {"x": 0, "y": 0, "z": 0}

# Parameters of the lug
parameters = {}
parameters["d1"] = [0.01, 0.12]
# parameters.append["D2", 0, 4]
# parameters.append["A2", 0, 4]
# parameters.append(["A3", 0, 4])
# parameters.append["A5", 0, 4]
parameters["t1"] = [0.0001, 0.05]
# parameters.append["t2", 0, 4]
# parameters.append["t3", 0, 4]
# parameters.append["h", 0, 4]
parameters["w"] = [0.051, 0.4]
parameters["e"] = [0.05, 0.1]
# parameters.append["n_holes", 0, 4]

print(parameters)

multiple_flanges = True


F_z = 1220  # Newton
F_y = 430  # Newton

safety_factor = 1.2

if multiple_flanges:
    F_y /= 2
    F_z /= 2


angle_z = math.tanh(F_y / F_z)  # Radians

# Point force P
# Angle_z is the angle with the z axis
p = {"magnitude": 0, "angle_z": angle_z}  # magnitude in N, angle in rad

p["magnitude"] = math.sqrt(F_z**2 + F_y**2)

steps = 30


for key, value in parameters.items():
    parameters[key].append(value[0])


def gen():
    highestFunctionOutput = 0
    highestFunctionOutput2 = 0

    lowestMass = 99999999

    highestParams = {}

    for k in range(steps ** len(parameters)):
        loopedParameters = []
        for i, (key, value) in enumerate(parameters.items()):
            value[2] = value[0] + math.floor(k % (steps ** (i + 1)) / steps**i) * (
                value[1] - value[0]
            ) / (steps - 1)
        result = calculate_max_y_transverse(
            parameters["d1"][2],
            parameters["t1"][2],
            parameters["w"][2],
            parameters["e"][2],
        )

        mass = calculate_mass(
            parameters["d1"][2],
            parameters["t1"][2],
            parameters["w"][2],
            parameters["e"][2],
        )

        result2 = calculate_shear_bearing_failure_axial(
            parameters["d1"][2],
            parameters["t1"][2],
            parameters["w"][2],
            parameters["e"][2],
        )
        if (
            mass != None
            and result > safety_factor * (F_z)
            and result2 > safety_factor * (F_y)
            and mass < lowestMass
        ):
            highestFunctionOutput = result
            highestFunctionOutput2 = result2

            lowestMass = mass

            for key, value in parameters.items():
                highestParams[key] = parameters[key][2]
    for key, value in highestParams.items():
        print(f"{key}: {value}")

    print(f"Mass: {lowestMass}")

    print(f"Force: {highestFunctionOutput}")
    print(f"Shear bear force: {highestFunctionOutput2}")
    if user_input == None:
        user_input = input("Save these parameters? (y/n) ")

    if str(user_input) == "y":
        with open("4.3_results.txt", "w") as f:
            for key, value in highestParams.items():
                f.write(f"{key}: {value}\n")
            f.write(f"Mass: {lowestMass} (kg)\n")
            f.write(f"Force: {highestFunctionOutput} (N)\n")
            f.write(f"Shear bear force: {highestFunctionOutput2} (N)\n")


# beginTime = time.time()
# gen()
# endTime = time.time() - beginTime
# print(f"Time it took: {round(endTime,2)} seconds.")


# def max_min(_min, _max, value):
#     max(_min, min(_max, value))
