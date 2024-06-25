# me - this DAT
# scriptOp - the OP which is cooking
import numpy as np
import math
# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(scriptOp):
	page = scriptOp.appendCustomPage('Custom')
	p = page.appendPulse('Vector', label='Set Vector')
      
	return

# called whenever custom pulse parameter is pushed
def onPulse(par):
    return


def onCook(scriptOp):
    scriptOp.clear()
    magical_function(scriptOp)
    return


def magical_function(scriptOp):
    
    #Take inputs and convert to vectors for easy dot/cross product
    target = scriptOp.inputs[0].numpyArray()[0:3]
    up = scriptOp.inputs[1].numpyArray()[0:3]
    rest = scriptOp.inputs[2].numpyArray()[0:3]

    target = tdu.Vector(target)
    up = tdu.Vector(up)
    rest = tdu.Vector(rest)


    #In the event that the 'resting' position is not orthogonal to the mount, find one that is
    rest_proj = rest.dot(up) / up.dot(up) * up
    forward = rest - rest_proj
    rest.normalize()

    #Projections to compress target into local XZ plane 
    proj = target.dot(up) / up.dot(up) * up
    floor_proj = target - proj

    #Send out information for rendering before we normalize
    out('proj', proj)
    out('floor_proj', floor_proj)
    out('rest', rest)
    op('distance').par.value0 = target.length()

    #Normalize stuff and declare down vector
    floor_proj.normalize()
    target.normalize()
    up.normalize()
    rest.normalize()
    forward.normalize()
    down = -up

    #Do the cross products to get direction
    cross_floor = forward.cross(floor_proj)
    left = forward.cross(up)

    #Find yaw through dot product cos(@)|A||B| = A . B --> acos(A.B/|A||B|) = @
    yaw = (math.acos(forward.dot(floor_proj))) #IMPORTANT STUFF

    if cross_floor.dot(up) < 0: #This is here to invert stuff since acos(180+x) = acos(x) so we have to mirror it
        yaw = math.pi*2-yaw                                              

    pitch = (math.acos(down.dot(target))) #IMPORTANT STUFF PART 2 (YOU THOUGHT WE WERE DONE SIKE) (its just the same as last time)
    #                                            But we dont need to do the inversion stuff cause the light cant bend backwards
    pitch -= math.acos(down.dot(rest))     #This is to get rid of the angle that the resting position is already turned from down

    #Send out the yaw and pitch in terms of degrees
    out_yaw = np.rad2deg(yaw)
    out_pitch = np.rad2deg(pitch)
    
    op('angle_output').par.value0 = out_yaw
    op('angle_output').par.value1 = out_pitch

    '''
    THIS IS FOR RENDERING ONLY (YOU CAN GET RID OF THIS TO IMPROVE PERFORMANCE SINCE IT USES SOME OF MATH)
    '''
    yaw *= -1
    #Rodrigues' rotation formula to rotate the down vector into all the other stuff
    pitched_vector = rest*math.cos(pitch) + (left.cross(rest))*math.sin(pitch) + left*(left.dot(rest))*(1-math.cos(pitch))
    yawed_and_pitched_vector = pitched_vector*math.cos(yaw) + down.cross(pitched_vector)*math.sin(yaw) + down*(down.dot(pitched_vector))*(1-math.cos(yaw))


    out('up', up)
    out('right', -left)
    out('forward', forward)

    out('pitched_v', pitched_vector)
    out('yawednpitched_v', yawed_and_pitched_vector)
    
    cross_floor.normalize()
    out('cross_product', cross_floor)

    return

def out(target, values):
    op(target).par.value0 = values[0]
    op(target).par.value1 = values[1]
    op(target).par.value2 = values[2]