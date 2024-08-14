'''
Changes angles based on 'center' s.t. you dont get any wonky 360 rotational things
'''
import math

data = op('cal')


def onOffToOn(channel, sampleIndex, val, prev):
    row = int(op('Selected')[0])
    center = data[row, 3]
    center *= math.pi

    if (center % 360) - 90 < 0 or (center % 360) + 90 > 360:
        op('add').par.value0 = 1
    else:
        op('add').par.value0 = 0
        
    return

def whileOn(channel, sampleIndex, val, prev):
    return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
	return