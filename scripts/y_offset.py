'''
changes tilt when clicking ui
'''

cal = op('cal')
out = op('Outraw')

def onOffToOn(channel, sampleIndex, val, prev):
	return

def whileOn(channel, sampleIndex, val, prev):
	cal[int(out[0]), 4] = round(cal[int(out[0]), 4] + (val - .2)*2, 2)
	return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
	return
	