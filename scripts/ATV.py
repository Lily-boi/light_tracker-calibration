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


    def angtovec(pan, tilt):
        ct = math.cos(tilt)
        st = math.sin(tilt)
        cp = math.cos(pan) 
        sp = math.sin(pan)
        return [ct*cp, st, ct*sp]

    target = angtovec(x, y)

    scriptOp.outputs[0].par.value0 = target[0]
    scriptOp.outputs[0].par.value1 = target[1]
    scriptOp.outputs[0].par.value2 = target[2]