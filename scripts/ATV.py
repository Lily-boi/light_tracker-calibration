'''
INPUT - Pan and Tilt (2 angles in deg)
OUTPUT - unit vector that has been rotated by the corrosponding pan and tilt
'''

import math
# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(scriptOp):
	return

# called whenever custom pulse parameter is pushed
def onPulse(par):
	return

def onCook(scriptOp):
	scriptOp.clear()
	convert(scriptOp)
	return

def convert(scriptOp):
    x = scriptOp.inputs[0][0]
    y = scriptOp.inputs[0][1]
    rtd = math.pi/180

    def angtovec(pan, tilt):
        ct = math.cos(rtd*tilt)
        st = math.sin(rtd*tilt)
        cp = math.cos(rtd*pan) #Negative here because rotations are counter clockwise but clockwise for the light
        sp = math.sin(rtd*pan)
        return [ct*cp, st, ct*sp]

    target = angtovec(x, y)

    scriptOp.outputs[0].par.value0 = target[0]
    scriptOp.outputs[0].par.value1 = target[1]
    scriptOp.outputs[0].par.value2 = target[2]