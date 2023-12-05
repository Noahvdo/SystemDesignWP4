import numpy as np
import math
#Pi in x and z
#myx= my*sin(a=38.5deg)
with open("WP4\SystemDesignWP4\Checks\Bearing\Results-4.7.txt", 'r') as file:
    lines = file.readlines()
D2 = float(lines[0].split()[-1])
t2 = float(lines[1].split()[-1])
Fx = float(lines[2].split()[-1])+float(lines[4].split()[-1])*math.sin(math.radians(38.5))
Fy = float(lines[3].split()[-1])+float(lines[4].split()[-1])*math.cos(math.radians(38.5))

Pi = np.array([Fx,Fy])


def magnitude(v):
    sum_squared=0
    for i in v:
        sum_squared+= i**2
    return math.sqrt(sum_squared)

def max_bearing_stress(Pi,D2,t2):
    return magnitude(Pi)/(D2*t2)

print(max_bearing_stress(Pi, D2 ,t2))



