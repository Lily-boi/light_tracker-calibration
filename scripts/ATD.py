'''
Converts incoming degrees and maps them to the light (This only works for amazon BEAM light)
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
	
	if (parent().par.Rot) & (x <= 180):
		x += 360

	pan_conv = 255/540
	tilt_conv = 1/1.04688


	x *= pan_conv
	x_floor = math.floor(x)
	x_fine = (x - x_floor) * 255	
	
	y *= tilt_conv
	y += 41.5302613
	y_floor = math.floor(y)
	y_fine = (y - y_floor) * 255

	scriptOp.outputs[0].par.value0 = x_floor
	scriptOp.outputs[0].par.value1 = x_fine
	scriptOp.outputs[0].par.value2 = y_floor
	scriptOp.outputs[0].par.value3 = y_fine
