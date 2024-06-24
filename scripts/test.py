# me - this DAT
# 
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
# 
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.
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
        ct = math.cos(rtd*pan)
        st = math.cos(rtd*tilt)
        cp = math.cos(rtd*pan)
        sp = math.sin(rtd*tilt)
        return(ct*cp, ct*sp, st)        

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
    out('true_position', solro)
    
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
