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
	return

def whileOn(channel, sampleIndex, val, prev):
    row = int(op('Selected')[0])
    if row:
        data[row, 3] = round(data[row, 3] + ((val - 2) / 90), 4)
    return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
    if val > 0:
        row = int(op('Selected')[0])
        if row:
            data[row, 3] = round(data[row, 3] + ((val - 2) / 90), 4)
    return
	