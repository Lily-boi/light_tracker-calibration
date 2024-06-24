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
	
	x *= .4737
	x_floor = math.floor(x)
	x_fine = (x - x_floor) * 255	

	y *= 1.17
	y_floor = math.floor(y)
	y_fine = (y - y_floor) * 255

	scriptOp.outputs[0].par.value0 = x_floor
	scriptOp.outputs[0].par.value1 = x_fine
	scriptOp.outputs[0].par.value2 = y_floor
	scriptOp.outputs[0].par.value3 = y_fine
