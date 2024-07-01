'''
Positional calibration system
Uses the dat table to get what pan and tilt the light needs to be to hit the light and what the point coords are

Lp = Light position
Pn = Point n position
Dn = Directional vector for point n
Lp = Pn - Rn(Dn)

Lp minimizes the difference between where it is and all the Pn-Rn(Dn) leading for a system of equations

'''
cal = op('cal')
out = op('Outraw')
import numpy as np
import math

def onOffToOn(channel, sampleIndex, val, prev):
    
    #Number of points
    n = 5
    rtd = math.pi/180
    vector = []
    points = []

    def angtovec(pan, tilt):
        pan *= 1
        tilt *= 1
        print(f'angles: {pan}, {tilt}')
        print(f'rad: {rtd*pan}, {rtd*tilt}')
        ct = math.cos(rtd*tilt)
        st = math.sin(rtd*tilt)
        cp = math.cos(rtd*pan)
        sp = math.sin(rtd*pan)
        return [ct*cp, st, ct*sp]

    #Looks for marked rows in the data sheet which signifies they contain a vector to be used
    print('---------------------------------------------------------')
    for row in range(n):
        vector.append(angtovec(float(cal[row+1,3]), float(cal[row+1,4])))
        
        points.append((float(cal[row+1,0]), float(cal[row+1,1]), float(cal[row+1,2])))
        
    def dot(u, v):
        n = len(u)
        s = 0
        for i in range(n):
            s += u[i]*v[i]
        return s


    A = [[0 for x in range(n+3)] for y in range(n+3)] 

    for i in range(n):
        A[i][i] = 1
    for i in range(3):
        A[i+n][i+n] = n

    for i in range(n):
        for j in range(3):
            A[i][n+j] = vector[i][j]
            A[n+j][i] = A[i][n+j]
    
    for row in A:
        print(row)
    B = [dot(points[i], vector[i]) for i in range(n)]

    for i in range(3):
        s = 0
        for j in range(n):
            s += points[j][i]
        B.append(s)

        
    solro = np.linalg.solve(A, B)
    print(solro[n:n+3])
    out('true_position', solro[n:n+3])
    
    out('vect', vector[0], points[0])
    out('vect1', vector[1], points[1])
    out('vect2', vector[2], points[2])
    out('vect3', vector[3], points[3])
    out('vect4', vector[4], points[4])
    return

def whileOn(channel, sampleIndex, val, prev):
	return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
	return

def out(target, val, val2 = None):
    opt = op(target)
    opt.par.value0 = val[0]
    opt.par.value1 = val[1]
    opt.par.value2 = val[2]
    if val2:
        opt.par.value3 = val2[0]
        opt.par.value4 = val2[1]
        opt.par.value5 = val2[2]

def normalize(v):
	norm = np.linalg.norm(v)
	if norm == 0: 
		return v
	return v / norm

def dot(u, v):
    print(u)
    w = 0
    for i in range(len(u)):
        w += (u[i] * v[i])
    
    return w
