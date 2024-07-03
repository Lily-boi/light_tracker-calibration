import numpy as np

def compute_R(phi, theta, beta):
    Rz_phi = np.array([[np.cos(phi), -np.sin(phi), 0],
                       [np.sin(phi), np.cos(phi), 0],
                       [0, 0, 1]])
    
    Ry_theta = np.array([[np.cos(theta), 0, np.sin(theta)],
                         [0, 1, 0],
                         [-np.sin(theta), 0, np.cos(theta)]])
    
    Rz_beta = np.array([[np.cos(beta), -np.sin(beta), 0],
                        [np.sin(beta), np.cos(beta), 0],
                        [0, 0, 1]])
    
    return Rz_phi @ Ry_theta @ Rz_beta
    
# me - this DAT
# scriptOp - the OP which is cooking

# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(scriptOp):
    page = scriptOp.appendCustomPage('Custom')
    p = page.appendFloat('Valuea', label='Value A')
    p = page.appendFloat('Valueb', label='Value B')
    rotate(scriptOp)
    return

# called whenever custom pulse parameter is pushed
def onPulse(par):
	return

def onCook(scriptOp):
    scriptOp.clear()
    rotate(scriptOp)
    return


def rotate(scriptOp):
    vec = scriptOp.inputs[0].numpyArray()
    rot = scriptOp.inputs[1].numpyArray()
    r = compute_R(rot[0][0], rot[1][0], rot[2][0])
    
    rVec = r @ vec
    
    scriptOp.outputs[0].par.value0 = rVec[0]
    scriptOp.outputs[0].par.value1 = rVec[1]
    scriptOp.outputs[0].par.value2 = rVec[2]