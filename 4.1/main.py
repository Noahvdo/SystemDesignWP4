import numpy as np
import math
from determine_dimensions import (
    calculate_max_y_transverse,
    calculate_shear_bearing_failure_axial,
)
from determine_mass import calculate_mass
import time

# Load forces

loads = {"x": 0, "y": 0, "z": 0}

# Moment forces

moments = {"x": 0, "y": 0, "z": 0}

# Parameters of the lug
min_max_parameters = {}
min_max_parameters["d1"] = [0.01, 0.12]
# min_max_parameters.append["D2", 0, 4]
# min_max_parameters.append["A2", 0, 4]
# min_max_parameters.append(["A3", 0, 4])
# min_max_parameters.append["A5", 0, 4]
min_max_parameters["t1"] = [0.0001, 0.05]
# min_max_parameters.append["t2", 0, 4]
# min_max_parameters.append["t3", 0, 4]
# min_max_parameters.append["h", 0, 4]
min_max_parameters["w"] = [0.051, 0.4]
min_max_parameters["e"] = [0.05, 0.1]
# min_max_parameters.append["n_holes", 0, 4]


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

steps = 15


def calculate_t2(shear_str):
    t_axial = (26729.29 + (26729.29**2 + 4 * shear_str * 5024.5) ** 0.5) / (
        2 * shear_str
    )
    t_shear = (
        5166.7308 + (5166.73**2 + 4 * shear_str * 0.5 * 159.93) ** 0.5
    ) / shear_str

    return max(t_axial, t_shear)


for key, value in parameters.items():
    parameters[key].append(value[0])

# "name", density (kg/m^3), tensile yield strength (MPa), ultimate tensile strength (MPa), yield bearing strength (MPa), ultimate bearing strength (MPa), shear strength (MPa)
material = [
    [
        "AL6061",
        2700,
        276 * 10**6,
        310 * 10**6,
        386 * 10**6,
        607 * 10**6,
        207 * 10**6,
    ],
    [
        "AL2024",
        2780,
        324 * 10**6,
        469 * 10**6,
        441 * 10**6,
        814 * 10**6,
        283 * 10**6,
    ],
]


def gen(parameters):
    highestFunctionOutput = 0
    highestFunctionOutput2 = 0
    lowestMass = 99999999
    highestParams = {}
    best_material = []

    for key, value in parameters.items():
        parameters[key].append(value[0])

    for lugmaterial in range(len(material)):
        t2 = calculate_t2(material[lugmaterial][6])
        for k in range(steps ** len(parameters)):
            loopedParameters = []
            for i, (key, value) in enumerate(parameters.items()):
                value[2] = value[0] + math.floor(
                    k % (steps ** (i + 1)) / steps**i
                ) * (value[1] - value[0]) / (steps - 1)
            result = calculate_max_y_transverse(
                parameters["d1"][2],
                parameters["t1"][2],
                parameters["w"][2],
                parameters["e"][2],
                material[lugmaterial][2],
            )

            mass = calculate_mass(
                parameters["d1"][2],
                parameters["t1"][2],
                parameters["w"][2],
                parameters["e"][2],
                material[lugmaterial][1],
                t2,
            )

            result2 = calculate_shear_bearing_failure_axial(
                parameters["d1"][2],
                parameters["t1"][2],
                parameters["w"][2],
                parameters["e"][2],
                material[lugmaterial][3],
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
                best_material = material[lugmaterial]
                for key, value in parameters.items():
                    highestParams[key] = parameters[key][2]
        result = {
            "Mass": lowestMass,
            "Force": highestFunctionOutput,
            "Shear bear force": highestFunctionOutput2,
            "Parameters": highestParams,
            "Material": best_material[0],
        }
        # for key, value in highestParams.items():
        #     print(f"{key}: {value}")

        # print(f"Mass: {lowestMass}")

        # print(f"Force: {highestFunctionOutput}")
        # print(f"Shear bear force: {highestFunctionOutput2}")

        # user_input = input("Save these parameters? (y/n) ")

        # if str(user_input) == "y":
        #     with open("4.3_results.txt", "w") as f:
        #         for key, value in highestParams.items():
        #             f.write(f"{key}: {value}\n")
        #         f.write(f"Mass: {lowestMass} (kg)\n")
        #         f.write(f"Force: {highestFunctionOutput} (N)\n")
        #         f.write(f"Shear bear force: {highestFunctionOutput2} (N)\n")
        return result


def max_min(_min, _max, value):
    return max(_min, min(_max, value))


deltaChange = 1.2
iteration_times = 7
beginTime = time.time()
parameters = min_max_parameters
for i in range(iteration_times):
    result = gen(parameters)
    if i == (iteration_times - 1):
        print(result)
        break
    parameters = result["Parameters"]
    for key, value in parameters.items():
        change = 1 + (10 ** (-i) * deltaChange)
        value_plus_change = max_min(
            min_max_parameters[key][0], min_max_parameters[key][1], value * change
        )
        value_minus_change = max_min(
            min_max_parameters[key][0], min_max_parameters[key][1], value / change
        )
        if key == "d1":
            print(key)
            print(value_minus_change, value_plus_change, value)
        # print(
        #     f"{key} change in next gen: {change}. With highest previous value: {value}"
        # )
        parameters[key] = [
            value_minus_change,
            value_plus_change,
            value_minus_change,
        ]
endTime = time.time() - beginTime
print(f"Time it took: {round(endTime,2)} seconds.")


# def max_min(_min, _max, value):
#     max(_min, min(_max, value))
