import math


def calculate_max_y_transverse(d, t, w):
    if w < d:
        return 0

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
    t_1 = t

    # Diameter of the hole
    d_1 = d

    A_1 = (
        0.5 * w - math.sqrt(1 / 8) * d_1
    ) * t_1  # (w / 2) - (d_1 / 2) * math.cos(math.pi / 4)
    A_2 = (w - d_1) / 2 * t_1
    A_3 = d_1 / 4 * t_1
    A_4 = A_1

    if A_1 == 0 or A_2 == 0 or A_3 == 0 or A_4 == 0:
        A_av = 0
    else:
        A_av = 6 / ((3 / A_1 + 1 / A_2 + 1 / A_3 + 1 / A_4))

    F_z = 1219  # Newton
    F_y = 430  # Newton

    angle_z = math.tanh(F_y / F_z)  # Radians

    # Point force P
    # Angle_z is the angle with the z axis
    p = {"magnitude": 0, "angle_z": angle_z}  # magnitude in N, angle in rad

    p["magnitude"] = math.sqrt(F_z**2 + F_y**2)

    A_br = d_1 * t_1

    K_ty = calculate_K_ty_transverse(A_av / A_br)

    # F_max_transverse = F_z / (A_br * K_ty)
    P_max_transverse = (A_br * K_ty) * 110 * (10**6) * A_br
    return P_max_transverse
    # print(F_max_transverse)


def calculate_shear_bearing_failure_axial(d, t, w, e):
    F_y = 430  # N
    A_br = d * t  # m^2

    # e is the length from the middle of the hole to the end.

    def calculate_kbry(x, t_over_d):
        return

    K_bry = calculate_kbry(e / d, t / d)

    F_tu = 310 * (10**6)  # Ultimate tensile strength (MPa)
    P_bry = K_bry * A_br * F_tu
    return P_bry
