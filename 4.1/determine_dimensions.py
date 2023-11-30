import math


def calculate_max_y_transverse(d, t, w, e, ultimate_yield):
    if w < d:
        return 0

    if e <= d / 2:
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

    A_1 = (0.5 * w - math.sqrt(1 / 8) * d_1) * t_1
    A_2 = (w - d_1) / 2 * t_1
    A_3 = (e - d / 2) * t_1
    A_4 = A_1

    if A_1 == 0 or A_2 == 0 or A_3 == 0 or A_4 == 0:
        A_av = 0
        k_ty = 0
        return 0
    else:
        A_av = 6 / ((3 / A_1 + 1 / A_2 + 1 / A_3 + 1 / A_4))
        A_br = d_1 * t_1
        K_ty = calculate_K_ty_transverse(A_av / A_br)

    P_max_transverse = (A_br * K_ty) * ultimate_yield * A_br
    return P_max_transverse


def calculate_shear_bearing_failure_axial(d, t, w, e, ultimate_tensile):
    F_y = 430  # N
    A_br = d * t  # m^2

    # e is the length from the middle of the hole to the end.

    def calculate_kbry(x, t_over_d):
        if t_over_d > 0.6:
            t_ovder_d = 0.6
        return (
            -9.4025514542896538 * 10 ** (0)
            + 4.0391421386558086 * x * 10 ** (1)
            - 6.7826122291138873 * x**2 * 10 ** (1)
            + 6.5286703940979805 * x**3 * 10 ** (1)
            - 3.8293403675800668 * x**4 * 10 ** (1)
            + 1.3901850817197953 * x**5 * 10 ** (1)
            - 3.0484378836593589 * x**6 * 10 ** (0)
            + 3.6985642168379590 * x**7 * 10 ** (-1)
            - 1.9058488395355754 * x**8 * 10 ** (-2)
        ) * (((-t_over_d + 0.06) / (0.54)) + 1) + (
            -6.6410559078902125 * 10 ** (0)
            + 2.8603157887923480 * x * 10 ** (1)
            - 5.1200641273277853 * x**2 * 10 ** (1)
            + 5.6882795611168881 * x**3 * 10 ** (1)
            - 3.8147040228991791 * x**4 * 10 ** (1)
            + 1.5471632347991896 * x**5 * 10 ** (1)
            - 3.7154463932966881 * x**6 * 10 ** (0)
            + 4.8626277555570813 * x**7 * 10 ** (-1)
            - 2.6723113554514642 * x**8 * 10 ** (-2)
        ) * (
            ((t_over_d - 0.06) / (0.54))
        )

    K_bry = calculate_kbry(e / d, t / d)

    # Ultimate tensile strength (MPa) aluminum 6061
    #F_tu = 310 * (10**6)
    P_bry = K_bry * A_br * ultimate_tensile * (w - d) * t
    return P_bry
