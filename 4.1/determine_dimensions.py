import numpy as np
import math


# D2 = float(lines[0].split()[-1])
# t2 = float(lines[1].split()[-1])
# Fx = float(lines[2].split()[-1])+float(lines[4].split()[-1])*math.sin(math.radians(38.5))
# Fy = float(lines[3].split()[-1])+float(lines[4].split()[-1])*math.cos(math.radians(38.5))


def magnitude(v):
    sum_squared = 0
    for i in v:
        sum_squared += i**2
    return math.sqrt(sum_squared)


def max_bearing_stress(D2, t2):
    Fx = float(26.91) + float(276.58) * math.sin(math.radians(38.5))
    Fy = float(76.25) + float(276.58) * math.cos(math.radians(38.5))
    Pi = np.array([Fx, Fy])
    return magnitude(Pi) / (D2 * t2)


# print(max_bearing_stress(Pi, D2 ,t2))


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

    P_max_transverse = (A_br * K_ty) * ultimate_yield
    return P_max_transverse


def calculate_shear_bearing_failure_axial(d, t, w, e, ultimate_tensile):
    F_y = 430  # N
    A_br = d * t  # m**2

    # e is the length from the middle of the hole to the end.

    def calculate_kbry(e_over_D, t_over_D):
        upperpart = 0
        lowerpart = 0
        if e_over_D < 0:
            e_over_D = 0
        elif e_over_D > 4:
            e_over_D = 3.99

        if t_over_D < 0.06:
            lowerpart = (
                -4.6896036256995037
                + 2.0120794261664585 * e_over_D * 10 ** (1)
                - 3.3717540932360293 * e_over_D**2 * 10 ** (1)
                + 3.2372334915435722 * e_over_D**3 * 10 ** (1)
                - 1.8927911100088579 * e_over_D**4 * 10 ** (1)
                + 6.8451588731258282 * e_over_D**5
                - 1.4941815748275624 * e_over_D**6
                + 1.8032464718216107 * e_over_D**7 * 10 ** (-1)
                - 9.2364056878591633 * e_over_D**8 * 10 ** (-3)
            )
        elif t_over_D >= 0.06 and t_over_D < 0.08:
            upper = (t_over_D - 0.06) / (0.08 - 0.06)

            lowerpart = (1 - upper) * (
                -4.6896036256995037
                + 2.0120794261664585 * e_over_D * 10 ** (1)
                - 3.3717540932360293 * e_over_D**2 * 10 ** (1)
                + 3.2372334915435722 * e_over_D**3 * 10 ** (1)
                - 1.8927911100088579 * e_over_D**4 * 10 ** (1)
                + 6.8451588731258282 * e_over_D**5
                - 1.4941815748275624 * e_over_D**6
                + 1.8032464718216107 * e_over_D**7 * 10 ** (-1)
                - 9.2364056878591633 * e_over_D**8 * 10 ** (-3)
            )
            upperpart = upper * (
                -2.9606988771450222
                + 1.0431307197540631 * e_over_D * 10 ** (1)
                - 1.2610009785538322 * e_over_D**2 * 10 ** (1)
                + 8.8039717881601014 * e_over_D**3
                - 3.6959902783596248 * e_over_D**4
                + 9.1719324161816784 * e_over_D**5 * 10 ** (-1)
                - 1.2372918614671038 * e_over_D**6 * 10 ** (-1)
                + 6.9851256086516777 * e_over_D**7 * 10 ** (-3)
            )
        elif t_over_D >= 0.08 and t_over_D < 0.10:
            upper = (t_over_D - 0.08) / (0.10 - 0.08)

            lowerpart = (1 - upper) * (
                -2.9606988771450222
                + 1.0431307197540631 * e_over_D * 10 ** (1)
                - 1.2610009785538322 * e_over_D**2 * 10 ** (1)
                + 8.8039717881601014 * e_over_D**3
                - 3.6959902783596248 * e_over_D**4
                + 9.1719324161816784 * e_over_D**5 * 10 ** (-1)
                - 1.2372918614671038 * e_over_D**6 * 10 ** (-1)
                + 6.9851256086516777 * e_over_D**7 * 10 ** (-3)
            )
            upperpart = upper * (
                -2.1981683101699012
                + 6.6146348368751724 * e_over_D
                - 5.5160179451650606 * e_over_D**2
                + 2.4412687369070092 * e_over_D**3
                - 5.8844302513719648 * e_over_D**4 * 10 ** (-1)
                + 7.2070228354446625 * e_over_D**5 * 10 ** (-2)
                - 3.4562859712813860 * e_over_D**6 * 10 ** (-3)
            )
        elif t_over_D >= 0.10 and t_over_D < 0.12:
            upper = (t_over_D - 0.10) / (0.12 - 0.10)

            lowerpart = (1 - upper) * (
                -2.1981683101699012
                + 6.6146348368751724 * e_over_D
                - 5.5160179451650606 * e_over_D**2
                + 2.4412687369070092 * e_over_D**3
                - 5.8844302513719648 * e_over_D**4 * 10 ** (-1)
                + 7.2070228354446625 * e_over_D**5 * 10 ** (-2)
                - 3.4562859712813860 * e_over_D**6 * 10 ** (-3)
            )
            upperpart = upper * (
                -2.0572659476609232
                + 6.0237666109177841 * e_over_D
                - 4.6639370878254853 * e_over_D**2
                + 1.9075886272245945 * e_over_D**3
                - 4.1813941358537965 * e_over_D**4 * 10 ** (-1)
                + 4.4804071921972721 * e_over_D**5 * 10 ** (-2)
                - 1.7125335198194085 * e_over_D**6 * 10 ** (-3)
            )
        elif t_over_D >= 0.12 and t_over_D < 0.15:
            upper = (t_over_D - 0.12) / (0.15 - 0.12)

            lowerpart = (1 - upper) * (
                -2.0572659476609232
                + 6.0237666109177841 * e_over_D
                - 4.6639370878254853 * e_over_D**2
                + 1.9075886272245945 * e_over_D**3
                - 4.1813941358537965 * e_over_D**4 * 10 ** (-1)
                + 4.4804071921972721 * e_over_D**5 * 10 ** (-2)
                - 1.7125335198194085 * e_over_D**6 * 10 ** (-3)
            )
            upperpart = upper * (
                -1.2567822098133723
                + 2.3896952457662444 * e_over_D
                + 1.5206094047075416 * e_over_D**2
                - 3.3138731411169564 * e_over_D**3
                + 2.0477692496833191 * e_over_D**4
                - 6.1952998449693286 * e_over_D**5 * 10 ** (-1)
                + 9.3847885768609959 * e_over_D**6 * 10 ** (-2)
                - 5.6983228949058643 * e_over_D**7 * 10 ** (-3)
            )
        elif t_over_D >= 0.15 and t_over_D < 0.2:
            upper = (t_over_D - 0.15) / (0.2 - 0.15)

            lowerpart = (1 - upper) * (
                -1.2567822098133723
                + 2.3896952457662444 * e_over_D
                + 1.5206094047075416 * e_over_D**2
                - 3.3138731411169564 * e_over_D**3
                + 2.0477692496833191 * e_over_D**4
                - 6.1952998449693286 * e_over_D**5 * 10 ** (-1)
                + 9.3847885768609959 * e_over_D**6 * 10 ** (-2)
                - 5.6983228949058643 * e_over_D**7 * 10 ** (-3)
            )
            upperpart = upper * (
                -1.3271679405321712
                + 3.0947216994475157 * e_over_D
                - 5.8102050958199036 * e_over_D**2 * 10 ** (-1)
                - 6.2957801761418630 * e_over_D**3 * 10 ** (-1)
                + 3.7958935015873302 * e_over_D**4 * 10 ** (-1)
                - 7.8743955018255027 * e_over_D**5 * 10 ** (-2)
                + 5.5966503396520885 * e_over_D**6 * 10 ** (-3)
                + 3.5694062212757346 * e_over_D**7 * 10 ** (-5)
            )
        elif t_over_D >= 0.2 and t_over_D < 0.3:
            upper = (t_over_D - 0.2) / (0.3 - 0.2)

            lowerpart = (1 - upper) * (
                -1.3271679405321712
                + 3.0947216994475157 * e_over_D
                - 5.8102050958199036 * e_over_D**2 * 10 ** (-1)
                - 6.2957801761418630 * e_over_D**3 * 10 ** (-1)
                + 3.7958935015873302 * e_over_D**4 * 10 ** (-1)
                - 7.8743955018255027 * e_over_D**5 * 10 ** (-2)
                + 5.5966503396520885 * e_over_D**6 * 10 ** (-3)
                + 3.5694062212757346 * e_over_D**7 * 10 ** (-5)
            )
            upperpart = upper * (
                -1.1879108982402455
                + 2.6623378029095295 * e_over_D
                - 2.3251479449582535 * e_over_D**2 * 10 ** (-1)
                - 6.3337926139087664 * e_over_D**3 * 10 ** (-1)
                + 3.1142860332613576 * e_over_D**4 * 10 ** (-1)
                - 5.7734055733136218 * e_over_D**5 * 10 ** (-2)
                + 3.8641594682388286 * e_over_D**6 * 10 ** (-3)
            )
        elif t_over_D >= 0.3 and t_over_D < 0.4:
            upper = (t_over_D - 0.3) / (0.4 - 0.3)

            lowerpart = (1 - upper) * (
                -1.1879108982402455
                + 2.6623378029095295 * e_over_D
                - 2.3251479449582535 * e_over_D**2 * 10 ** (-1)
                - 6.3337926139087664 * e_over_D**3 * 10 ** (-1)
                + 3.1142860332613576 * e_over_D**4 * 10 ** (-1)
                - 5.7734055733136218 * e_over_D**5 * 10 ** (-2)
                + 3.8641594682388286 * e_over_D**6 * 10 ** (-3)
            )
            upperpart = upper * (
                -1.2583969710046172
                + 3.0355847622348842 * e_over_D
                - 9.4946187450785435 * e_over_D**2 * 10 ** (-1)
                - 8.1467692852381091 * e_over_D**3 * 10 ** (-3)
                + 5.1662720110212577 * e_over_D**4 * 10 ** (-2)
                - 6.5443327006986267 * e_over_D**5 * 10 ** (-3)
            )
        elif t_over_D >= 0.4 and t_over_D < 0.6:
            upper = (t_over_D - 0.4) / (0.6 - 0.4)

            lowerpart = (1 - upper) * (
                -1.2583969710046172
                + 3.0355847622348842 * e_over_D
                - 9.4946187450785435 * e_over_D**2 * 10 ** (-1)
                - 8.1467692852381091 * e_over_D**3 * 10 ** (-3)
                + 5.1662720110212577 * e_over_D**4 * 10 ** (-2)
                - 6.5443327006986267 * e_over_D**5 * 10 ** (-3)
            )
            upperpart = upper * (
                -1.2839908805028768
                + 3.1541259747416843 * e_over_D
                - 1.1384857426815129 * e_over_D**2
                + 1.1778920501144810 * e_over_D**3 * 10 ** (-1)
                + 1.7393111952747821 * e_over_D**4 * 10 ** (-2)
                - 3.2692480055983015 * e_over_D**5 * 10 ** (-3)
            )
        elif t_over_D >= 0.6:
            lowerpart = (
                -1.2839908805028768
                + 3.1541259747416843 * e_over_D
                - 1.1384857426815129 * e_over_D**2
                + 1.1778920501144810 * e_over_D**3 * 10 ** (-1)
                + 1.7393111952747821 * e_over_D**4 * 10 ** (-2)
                - 3.2692480055983015 * e_over_D**5 * 10 ** (-3)
            )

        return lowerpart + upperpart

    K_bry = calculate_kbry(e / d, t / d)

    P_bry = K_bry * A_br * ultimate_tensile #* (w - d) * t
    return P_bry
