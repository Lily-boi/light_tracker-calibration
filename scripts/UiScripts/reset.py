# me - this DAT
# 
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
# 
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.

data = op('cal')


def onOffToOn(channel, sampleIndex, val, prev):
    for i in range(data.numRows-1):
        data[i, 3] = 0
        data[i, 4] = 0
    
    parent().par.Mountedplanex = 0
    parent().par.Mountedplaney = 1
    parent().par.Mountedplanez = 0
    parent().par.Restingx = 1
    parent().par.Restingy = 0
    parent().par.Restingz = 0
    parent().par.Positionx = 0
    parent().par.Positiony = 0
    parent().par.Positionz = 0

def whileOn(channel, sampleIndex, val, prev):
    return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
    return
	