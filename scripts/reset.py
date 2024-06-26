'''For positional calibration, sets angles to 0, 0'''
cal = op('cal')
out = op('Outraw')

def onOffToOn(channel, sampleIndex, val, prev):
	cal[int(out[0]), 4] = 0
	cal[int(out[0]), 3] = 0
	cal[int(out[0]), 5] = 0
	return

def whileOn(channel, sampleIndex, val, prev):
	return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
	return
	