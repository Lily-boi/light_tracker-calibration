'''
Marks the row of the dat file to tell the scripts to use that point in the positional calibration system
'''
cal = op('cal')
out = op('Outraw')

def onOffToOn(channel, sampleIndex, val, prev):
	cal[int(out[0]), 6] = 1
	return

def whileOn(channel, sampleIndex, val, prev):
	return

def onOnToOff(channel, sampleIndex, val, prev):
	cal[int(out[0]), 6] = 0
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
	return
	