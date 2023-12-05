import numpy as np


def calculate_d2(w, d2_initial):
    # initial values:
    d2 = d2_initial  # diameter of the holes
    n = 4  # enter the number of fasteners vertically
    m = 2  # enter 2 for metal and 4 for composite
    WidthRequired = d2 * (3 + (n - 1) * m)
    WidthLimit = d2 * (3 + (n - 1) * (m + 1))

    if w < WidthRequired:
        # print("Back-up plate is not strong enough or the holes are too big.")
        while w < WidthRequired:
            WidthRequired = d2 * (3 + (n - 1) * m)
            d2 = d2 * 0.999
    elif w > WidthLimit:
        # print("The holes should be bigger.")
        while w > WidthLimit:
            WidthLimit = d2 * (3 + (n - 1) * (m + 1))
            d2 = d2 * 1.001

    return round(d2, 4)
    # print("d2 is now ", round(d2,4))
    # print("The area of the fasteners is about:", round(n * np.pi * 2500 * d2 * d2),"cm^2.")
