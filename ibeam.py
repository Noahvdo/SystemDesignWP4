import numpy as np
import math

iterations = 9
parameters = [["tb",0.00000001,0.2],["a",0.00000001,0.5],["tz",0.00000001,0.2]]

F = 430.5609  #N
stressy = 345*10**6  #Pa
D1 = 0.1
problem = 1

def givQ(tb,a,tz):
    if problem == 1:
        return a**2*(tz/8) + D1*tb*(a+tb)/2
    if problem == 2:
        return (D1**2-tz**2)*tb/8

def givI(tb,a,tz):
    if problem == 1:
        return 2*(1/12*tb*D1**3 + (D1/2)**2 * (tb*D1)) + 1/12 * a*tz**3
    if problem == 2:
        return (1/6*tb*D1**3)+1/12*a*tz**3

def area(tb,a,tz):
    return D1*tb*2+a*tz

def force(tb,Q,I):
    return 2*F*Q/(I*tb)


#0 = name   1 =  lower   2 = upper    3 = value

list = []
minarea = 999999999999999999
bestforce = 0
bestk = -1

for par in parameters:
    par.append(par[2])

for f in range(10):
    if f > 1:
        for i,par in enumerate(parameters):
            par[1] = list[i][1]*(1+25/(10**(f-1)))**-1
            par[2] = list[i][1]*(1+25/(10**(f-1)))
            if i == 2:
                print(i,par[1],list[i][1],par[2])
    for k in range(iterations**len(parameters)):
        for i,par in enumerate(parameters):
            par[3] = par[1] + math.floor(k%iterations**(i+1)/iterations**i)*(par[2]-par[1])/(iterations-1)

        if area(parameters[0][3],parameters[1][3],parameters[2][3]) < minarea and stressy > 1.2*force(parameters[0][3],givQ(parameters[0][3],parameters[1][3],parameters[2][3]),givI(parameters[0][3],parameters[1][3],parameters[2][3])):
            bestforce = 1.2*force(parameters[0][3] , givQ(parameters[0][3],parameters[1][3],parameters[2][3]) , givI(parameters[0][3],parameters[1][3],parameters[2][3]))
            minarea = area(parameters[0][3],parameters[1][3],parameters[2][3])
            bestk = k
            list = []
            for r in parameters:
                list.append([r[0],r[3]])
    



print(list,minarea,bestforce)


#parameters = [["tb",0.00002,0.000028],["a",0.000000001,0.005],["tz",0.000000001,0.0012],["y",0.000000001,0.0045]]
