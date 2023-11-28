import math

density = 2700  # aluminum 6061

L1 = 0.2
L2 = 0.1
# A = 0.05
holes = 0
h = 0.1


def calculate_mass(D1, t1, w, e):
    A = e - 0.5 * D1
    D2 = w / 5
    t2 = t1

    lug_volume = (
        w * L1 + 0.5 * math.pi * (0.5 * D1 + A) ** 2 - math.pi * (0.5 * D1) ** 2
    ) * t1

    plate_volume = ((h + 2 * t1 + 2 * L2) * w - holes * math.pi * (0.5 * D2) ** 2) * t2

    mass = (lug_volume * 2 + plate_volume) * density
    if mass < 0:
        return None
    return mass
