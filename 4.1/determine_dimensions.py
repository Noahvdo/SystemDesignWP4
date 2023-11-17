import math


def calculate_K_ty_transverse(x):
    """
    Parameters:
    x (float): Returns the K_ty value for the transverse load based on A_av/A_br
    """
    x = max(0, min(1.4, x))
    y = (
        -0.0046429324
        + 1.24667 * x
        + 0.2731277 * (x**2)
        - 0.769549 * (x**3)
        + 0.292853 * (x**4)
    )
    return y


# Thickness of the hole
t_1 = 1

# Diameter of the hole
d_1 = 1

# w in the picture
w = 1

A_1 = d_1 * math.cos(math.pi / 4) - d_1 + (w - d_1)  # Centimeters
A_2 = 1  # Centimeters
A_3 = 1  # Centimeters
A_4 = A_1  #

F_z = 600  # Newton
F_y = 800  # Newton

angle_z = math.tanh(F_y / F_z)  # Radians

# Point force P
# Angle_z is the angle with the z axis
p = {"magnitude": 0, "angle_z": angle_z}  # magnitude in N, angle in rad

p["magnitude"] = math.sqrt(F_z**2 + F_y**2)

A_br = d_1 * t_1
A_av = 6 / (3 / A_1 + 1 / A_2 + 1 / A_3 + 1 / A_4)

K_ty = calculate_K_ty_transverse(A_br / A_av)

F_max_transverse = p["magnitude"] / (A_br * K_ty)

print(F_max_transverse)


# A_br = t_1 * D1
# A_av = 6 / (3 / A_1 + 1 / A_2 + 1 / A_3 + 1 / A_4)
