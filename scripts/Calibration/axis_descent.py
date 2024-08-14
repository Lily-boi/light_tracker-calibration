import numpy as np

def compute_R(params):
    # Computes rotational matrix R (The orientation of the light)
    beta, theta, phi = params
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

def distance(params, points, directions):
    # Computes how far off the R is by summing the distance between calculated 
    # points and actual points
    R = compute_R(params)
    rotated_directions = directions @ R.T
    distances = np.linalg.norm(points - rotated_directions, axis=1)
    return np.sum(distances)

def gradient_descent(points, directions, learning_rate=0.01, iterations=1000):
    params = np.array([0.0, 0.0, 0.0])
    for i in range(iterations):
        cost = distance(params, points, directions)
        grad = np.zeros(3)
        epsilon = 1e-5
        
        for j in range(3):
            params_eps = np.copy(params)
            params_eps[j] += epsilon
            cost_eps = distance(params_eps, points, directions)
            grad[j] = (cost_eps - cost) / epsilon
        
        params -= learning_rate * grad
        
        if np.linalg.norm(grad) < 1e-6:
            break
    
    return compute_R(params)

def run(points, directions):

    R = gradient_descent(points, directions)
    up = R @ np.array([0, 1, 0])
    rest = R @ np.array([1, 0, 0])


    parent().par.Mountedplanex = up[0]
    parent().par.Mountedplaney = up[1]
    parent().par.Mountedplanez = up[2]
    parent().par.Restingx = rest[0]
    parent().par.Restingy = rest[1]
    parent().par.Restingz = rest[2]
