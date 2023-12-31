import numpy as np
import math
from functions.determine_loads import (
    calculate_max_y_transverse,
    calculate_shear_bearing_failure_axial,
    max_bearing_stress,
)
from functions.determine_mass import calculate_mass
import time
from functions.d2_calculator import calculate_d2

# Parameters of the lug
min_max_parameters = {}
min_max_parameters["d1"] = [0.1, 0.17]
min_max_parameters["t1"] = [0.00001, 0.004]
min_max_parameters["w"] = [0.183, 0.4]
min_max_parameters["e"] = [0.02, 0.1]


multiple_flanges = True


F_z = 1220  # Newton
F_y = 430  # Newton

safety_factor = 1.2

if multiple_flanges:
    F_y /= 2
    F_z /= 2

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
    [
        "Ti-6Al-4V",
        4430,
        113.8 * 10**9,
        44 * 10**9,
        880 * 10**6,
        950 * 10**6,
        1480 * 10**6,
        1860 * 10**6,
    ],
    [
        "S-2 Glass Fibre",
        2460,
        86.9 * 10**9,
        35 * 10**9,
        3660 * 10**6,
        4590 * 10**6,
        86 * 10**6,
        150 * 10**6,
    ],
    [
        "AA 7178-T6",
        2830,
        71.7 * 10**9,
        27 * 10**9,
        538 * 10**6,
        607 * 10**6,
        807 * 10**6,
        1089 * 10**6,
    ],
]


def gen(parameters):
    highestFunctionOutput = 0
    highestFunctionOutput2 = 0
    highestFunctionOutput3 = 0
    lowestMass = 99999999
    highestParams = {}
    best_material = []
    t2_best = 0
    d2 = 0.02

    for key, value in parameters.items():
        parameters[key].append(value[0])

    for lugmaterial in range(len(material)):
        t2 = calculate_t2(material[lugmaterial][4])

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
                material[lugmaterial][4],
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
                material[lugmaterial][5],
            )
            result3 = max_bearing_stress(d2, t2)
            if (
                mass != None
                and result > safety_factor * (F_z)
                and result2 > safety_factor * (F_y)
                and result3 < safety_factor * material[lugmaterial][6]
                and mass < lowestMass
                and parameters["d1"][2] / 2 < parameters["e"][2] + 0.001
            ):
                highestFunctionOutput = result
                highestFunctionOutput2 = result2
                highestFunctionOutput3 = result3
                lowestMass = mass
                best_material = material[lugmaterial]
                for key, value in parameters.items():
                    highestParams[key] = parameters[key][2]
                t2_best = t2
        result = {
            "Mass": lowestMass,
            "Force": highestFunctionOutput,
            "Shear bear force": highestFunctionOutput2,
            "Max bearing strength": highestFunctionOutput3,
            "Parameters": highestParams,
            "t2": t2_best,
            "d2": d2,
            "Material": best_material[0],
        }
        return result


def max_min(_min, _max, value):
    return max(_min, min(_max, value))


def handle_results(result):
    parameters = result["Parameters"]
    mass = result["Mass"]
    force = result["Force"]
    force_safety_margin = force/F_z
    shear_bear_force = result["Shear bear force"]
    shear_force_safety_margin = force/F_y
    max_bearing_stress = result["Max bearing strength"]
    t2 = result["t2"]
    d2 = result["d2"]
    material = result["Material"]

        \
    
    for key, value in parameters.items():
        print(f"{key}: {value}")
    print(f"t2: {t2}")
    print(f"d2: {d2}")
    print(f"Mass: {mass}")

    print(f"Transverse yield strength: {force}. Safety margin: {force_safety_margin}")
    print(f"Shear bear force: {shear_bear_force}. Safety margin: {shear_force_safety_margin}")
    print(f"Max bearing stress: {max_bearing_stress}")
    print(f"Material: {material}")

    user_input = input("Save these parameters? (y/n) ")

    if str(user_input) == "y":
        with open("results/results.txt", "w") as f:
            for key, value in parameters.items():
                f.write(f"{key}: {value}\n")
            f.write(f"t2: {t2}\n")
            f.write(f"d2: {d2}\n")
            f.write(f"Mass: {mass} (kg)\n")
            f.write(f"Transverse yield strength: {force} (N). Safety margin: {force_safety_margin}\n")
            f.write(f"Shear bear force: {shear_bear_force} (N). Safety margin: {shear_force_safety_margin}\n")
            f.write(f"Max bearing stress: {max_bearing_stress} (N)\n")
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
