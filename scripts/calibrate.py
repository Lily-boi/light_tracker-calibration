import math, numpy as np
cal = op('cal')
def onOffToOn(channel, sampleIndex, val, prev):



	return

def whileOn(channel, sampleIndex, val, prev):
	return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
	return
	
    
'''
Rules/Ideas:

If everything is offset by a constant, shift the position of the light. 

If there is discrepency on the tilt of the side axis, the mounted plane is not level and should be adjusted accordingly

If there is offset in the same direction but not constante, the resting angle is off

Scenario 1:
Offset downwards that gets larger the further the targets are
Offset less so on the outer points



average the offset --> thats your relative position



Idea:
Draw lines from each offset point, 
'''