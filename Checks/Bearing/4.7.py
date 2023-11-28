import numpy as np
import math
Pi = np.array([[1,2,3],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]])
with open("Checks\Bearing\Results-4.7.txt", 'r') as file:
    lines = file.readlines()
D2 = float(lines[0].split()[-1])
t2 = float(lines[1].split()[-1])

def magnitude(v):
    sum_squared=0
    for i in v:
        sum_squared+= i**2
    return math.sqrt(sum_squared)

def max_bearing_stress(Pi,D2,t2):
    mags=[]
    for i in Pi:
        mags += [magnitude(i)]
    P=max(mags)
    return P/(D2*t2)

max_bearing_stress(Pi,D2,t2)


