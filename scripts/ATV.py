# me - this DAT
# scriptOp - the OP which is cooking
import math
# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(scriptOp):
	page = scriptOp.appendCustomPage('Custom')
	p = page.appendFloat('Valuea', label='Value A')
	p = page.appendFloat('Valueb', label='Value B')
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
        cp = math.cos(rtd*-pan)
        sp = math.sin(rtd*-pan)
        return [ct*cp, st, ct*sp]

    target = angtovec(x, y)

    scriptOp.outputs[0].par.value0 = target[0]
    scriptOp.outputs[0].par.value1 = target[1]
    scriptOp.outputs[0].par.value2 = target[2]