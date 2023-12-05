import numpy as np
import math
from determine_dimensions import (
    calculate_max_y_transverse,
    calculate_shear_bearing_failure_axial,
    max_bearing_stress,
)
from determine_mass import calculate_mass
import time
from d2_calculator import calculate_d2

# Parameters of the lug
min_max_parameters = {}
min_max_parameters["d1"] = [0.01, 0.15]
# min_max_parameters.append["D2", 0, 4]
# min_max_parameters.append["A2", 0, 4]
# min_max_parameters.append(["A3", 0, 4])
# min_max_parameters.append["A5", 0, 4]
min_max_parameters["t1"] = [0.0001, 0.05]
# min_max_parameters.append["t2", 0, 4]
# min_max_parameters.append["t3", 0, 4]
# min_max_parameters.append["h", 0, 4]
min_max_parameters["w"] = [0.183, 0.4]
min_max_parameters["e"] = [0.02, 0.1]
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


# "name", density (kg/m^3), Young's Modulus (Pa), Shear's Modulus (Pa), tensile yield strength (Pa), ultimate tensile strength (Pa), yield bearing (Pa), ultimate bearing (Pa)
material = [
    [
        "AL6061",
        2700,
        68.9 * 10**9,
        26 * 10**9,
        276 * 10**6,
        310 * 10**6,
        386 * 10**6,
        607 * 10**6,
    ],
    [
        "AL2024",
        2780,
        73.1 * 10**9,
        28 * 10**9,
        324 * 10**6,
        469 * 10**6,
        441 * 10**6,
        814 * 10**6,
    ],
]  # ,["304 stainless steel",8000,193*10**9,77*10**9,215*10**6,505*10**6,-,-]]


def gen(parameters):
    highestFunctionOutput = 0
    highestFunctionOutput2 = 0
    lowestMass = 99999999
    highestParams = {}
    best_material = []
    t2_best = 0
    d2_init = 2
    d2_best = 0

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

            result3 = max_bearing_stress(0.02, t2)
            if (
                mass != None
                and result > safety_factor * (F_z)
                and result2 > safety_factor * (F_y)
                and result3 < safety_factor * material[lugmaterial][6]
                and mass < lowestMass
            ):
                highestFunctionOutput = result
                highestFunctionOutput2 = result2
                d2_best = calculate_d2(parameters["w"][2], d2_init)
                lowestMass = mass
                best_material = material[lugmaterial]
                for key, value in parameters.items():
                    highestParams[key] = parameters[key][2]
                t2_best = t2
        result = {
            "Mass": lowestMass,
            "Force": highestFunctionOutput,
            "Shear bear force": highestFunctionOutput2,
            "Parameters": highestParams,
            "t2": t2_best,
            "d2": d2_best,
            "Material": best_material[0],
        }
        return result


def max_min(_min, _max, value):
    return max(_min, min(_max, value))


def handle_results(result):
    parameters = result["Parameters"]
    mass = result["Mass"]
    force = result["Force"]
    shear_bear_force = result["Shear bear force"]
    t2 = result["t2"]
    d2 = result["d2"]
    material = result["Material"]

    for key, value in parameters.items():
        print(f"{key}: {value}")
    print(f"t2: {t2}")
    print(f"d2: {d2}")
    print(f"Mass: {mass}")

    print(f"Force: {force}")
    print(f"Shear bear force: {shear_bear_force}")
    print(f"Material: {material}")

    user_input = input("Save these parameters? (y/n) ")

    if str(user_input) == "y":
        with open("results.txt", "w") as f:
            for key, value in parameters.items():
                f.write(f"{key}: {value}\n")
            f.write(f"t2: {t2}\n")
            f.write(f"d2: {d2}\n")
            f.write(f"Mass: {mass} (kg)\n")
            f.write(f"Force: {force} (N)\n")
            f.write(f"Shear bear force: {shear_bear_force} (N)\n")
            f.write(f"Material: {material}")


deltaChange = 1.2
iteration_times = 7
beginTime = time.time()
parameters = min_max_parameters
for i in range(iteration_times):
    result = gen(parameters)
    if i == (iteration_times - 1):
        handle_results(result)
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
        parameters[key] = [
            value_minus_change,
            value_plus_change,
            value_minus_change,
        ]
endTime = time.time() - beginTime
print(f"Time it took: {round(endTime,2)} seconds.")


# def max_min(_min, _max, value):
#     max(_min, min(_max, value))
