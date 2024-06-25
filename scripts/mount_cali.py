# me - this DAT
# scriptOp - the OP which is cooking
import numpy as np
# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(scriptOp):
    angle(scriptOp)
    return

# called whenever custom pulse parameter is pushed
def onPulse(par):
    return

def onCook(scriptOp):
    scriptOp.clear()
    return


def angle(scriptOp):
    angleZ = float(scriptOp.inputs[0][1]) or 0
    angleX = -float(scriptOp.inputs[0][0]) or 0

    angleX = np.deg2rad(angleX)
    angleZ = np.deg2rad(angleZ)

    u = np.array([np.cos(angleX), np.sin(angleX), 0])
    v = np.array([0, np.sin(angleZ), np.cos(angleZ)])
    n = np.cross(v, u) 
    

    out('x_norm', u)
    out('z_norm', v)
    out('up_norm', n)


def out(target, var):
    op(target).par.value0 = var[0]
    op(target).par.value1 = var[1]
    op(target).par.value2 = var[2]