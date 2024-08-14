# me - this DAT
# 
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
# 
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.
import numpy as np

data = op('cal')

def ATV(pt):
    pan, tilt = pt
    ct = np.cos(tilt)
    st = np.sin(tilt)
    cp = np.cos(pan) 
    sp = np.sin(pan)
    return [ct*cp, st, ct*sp]


def data_get(row, cols, cole=0):
        cole = cole or cols + 2
        sample = []
        for i in range(cols, cole+1):
            sample.append(float(data[row, i]))
        return sample

def onOffToOn(channel, sampleIndex, val, prev):
    run_me = mod('axis').run
    points = []
    directions = []
    for i in [1, 2, 3]:
        points.append(data_get(i, 0))
        directions.append(ATV(data_get(i, 3, 4)))
    
    
    run_me(np.array(points), np.array(directions))
    
    return

def whileOn(channel, sampleIndex, val, prev):
    return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
    return