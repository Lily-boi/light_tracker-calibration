# me - this DAT
# 
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
# 
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.
cal = op('cal')
out = op('Outraw')
import numpy as np

def onOffToOn(channel, sampleIndex, val, prev):
	vectors = []
	vector_point = []

	#Looks for marked rows in the data sheet which signifies they contain a vector to be used

	for row in range(8):
		if cal[row+1, 6] == 1:
	
			array = np.array([float(cal[row+1,3]), float(cal[row+1,4]), float(cal[row+1,5])])
			vectors.append(array)
			vector_point.append(np.array([float(cal[row+1, 0]), float(cal[row+1, 1]), float(cal[row+1, 2])]))
	
	#Pick the first 3 vectors and calculate normal vectors between all of them
	u, v, w = vectors[0:3]
	norm1 = np.cross(u, v)
	norm2 = np.cross(v, w)
	norm3 = np.cross(w, u)
	norms = [norm1, norm2, norm3]
	#U, V, W are normal's
	#vector_point contains the corrosponding points that are on each plane

	A = np.vstack(norms)
	print(A.shape)
	if np.linalg.det(A) == 0:
		print('Pick some better points, stupid')
		return
	b = np.array([vec.dot(point) for vec, point in zip(norms, vector_point)])
	
	try:
		interesction = np.linalg.solve(A, b)
	except:
		interesction = 'error'

	print(interesction)
	
	op('true_position').par.value0 = interesction[0]
	op('true_position').par.value1 = interesction[1]
	op('true_position').par.value2 = interesction[2]

	op('calibrating').par.value0 = 0
	return

def whileOn(channel, sampleIndex, val, prev):
	return

def onOnToOff(channel, sampleIndex, val, prev):
	return

def whileOff(channel, sampleIndex, val, prev):
	return

def onValueChange(channel, sampleIndex, val, prev):
	return
	