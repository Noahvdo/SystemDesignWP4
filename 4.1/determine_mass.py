import math

#density = 2700  # aluminum 6061

L1 = 0.2
#L2 = 0.1
# A = 0.05
holes = 8
#h = 0.12
D2 = 0.02

def calculate_mass(D1, t1, w, e, rho, t2):
    lug_width = (0.07543 + 1.5*D2)*2  #(h + 2 * t1 + 2 * L2)
    density = rho
    A = e - 0.5 * D1

    flange_volume = (
        w * L1 + 0.5 * math.pi * (0.5 * D1 + A) ** 2 - math.pi * (0.5 * D1) ** 2
    ) * t1

    plate_volume = (lug_width * w - holes * math.pi * (0.5 * D2) ** 2) * t2

    mass = (flange_volume * 2 + plate_volume) * density
    if mass < 0:
        return None
    return mass
