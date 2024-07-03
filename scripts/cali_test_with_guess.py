import numpy as np
import math

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def out(target, val, val2=None):
    opt = op(target)
    opt.par.value0 = val[0]
    opt.par.value1 = val[1]
    opt.par.value2 = val[2]
    if val2:
        opt.par.value3 = val2[0]
        opt.par.value4 = val2[1]
        opt.par.value5 = val2[2]

def ATV(pt):
    pan, tilt = pt
    ct = math.cos(tilt)
    st = math.sin(tilt)
    cp = math.cos(pan) 
    sp = math.sin(pan)
    return [ct * cp, st, ct * sp]

def onSetupParameters(scriptOp):
    page = scriptOp.appendCustomPage('Custom')
    p = page.appendPulse('Calibrate', label='Calibrate')
    return

def onPulse(par):
    data = op('cal')
    
    def data_get(row, cols, cole=0):
        cole = cole or cols + 2
        sample = []
        for i in range(cols, cole + 1):
            sample.append(float(data[row, i]))
        return sample
    
    if par:
        V = []
        u = []
        for n in range(1, data.numRows):
            if int(data_get(n, 5, 5)[0]) == 1:
                v_ = data_get(n, 0)
                u_ = ATV(data_get(n, 3, 4))
                V.append(v_)
                u.append(u_)
                out(f'vect{n}', u_, v_)
        
        V = np.array(V)
        u = np.array(u)

        # Estimate the initial up vector from the scale on the light
        scale_tilt = 0.1  # Example tilt angle from the scale on the light
        scale_pan = 0.2  # Example pan angle from the scale on the light
        up_vector = estimate_up_vector(scale_tilt, scale_pan)
        
        # Estimate initial guess for phi, theta, beta
        phi_init, theta_init, beta_init = initial_guess_up_vector(up_vector, V, u)

        # Perform optimization
        phi_opt, theta_opt, beta_opt = newton_raphson_multi(phi_init, theta_init, beta_init, V, u)

        print(f"Optimal phi: {phi_opt}\ntheta: {theta_opt}\nbeta: {beta_opt}")
        
        p0 = compute_p0(compute_R(phi_opt, theta_opt, beta_opt), V, u)
        r = compute_R(phi_opt, theta_opt, beta_opt)
        
        print(f'Optimal p0: {p0} \nR: {r}')
        
        up = np.array([0, 1, 0])
        up = normalize(r @ up)
        print(f'Up: {up}')
        resting = np.array([op('resting')[0], op('resting')[1], op('resting')[2]])
        resting = normalize(r @ resting)
        print(f'Resting: {resting}')
        
        out('mount_plane', up)
        out('resting_pos', resting)
        out('true_position', p0)
        
        for n, i in enumerate(u):
            i = r @ i
            op(f'vect{n+1}').par.value6 = i[0]
            op(f'vect{n+1}').par.value7 = i[1]
            op(f'vect{n+1}').par.value8 = i[2]

def onCook(scriptOp):
    scriptOp.clear()
    return

def estimate_up_vector(scale_tilt, scale_pan):
    ct = math.cos(scale_tilt)
    st = math.sin(scale_tilt)
    cp = math.cos(scale_pan)
    sp = math.sin(scale_pan)
    return np.array([ct * cp, st, ct * sp])

def initial_guess_up_vector(up_vector, V, u):
    up_vector = normalize(up_vector)
    target_up = np.array([0, 1, 0])
    v = np.cross(up_vector, target_up)
    c = np.dot(up_vector, target_up)
    k = 1 / (1 + c)
    
    R_up = np.array([[v[0] * v[0] * k + c, v[0] * v[1] * k - v[2], v[0] * v[2] * k + v[1]],
                     [v[1] * v[0] * k + v[2], v[1] * v[1] * k + c, v[1] * v[2] * k - v[0]],
                     [v[2] * v[0] * k - v[1], v[2] * v[1] * k + v[0], v[2] * v[2] * k + c]])

    phi_init = math.atan2(R_up[1, 0], R_up[0, 0])
    theta_init = math.asin(-R_up[2, 0])
    beta_init = math.atan2(R_up[2, 1], R_up[2, 2])
    
    return phi_init, theta_init, beta_init

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

def partial_R_phi(phi, theta, beta):
    dRz_phi = np.array([[-np.sin(phi), -np.cos(phi), 0],
                        [np.cos(phi), -np.sin(phi), 0],
                        [0, 0, 0]])
    
    Ry_theta = np.array([[np.cos(theta), 0, np.sin(theta)],
                         [0, 1, 0],
                         [-np.sin(theta), 0, np.cos(theta)]])
    
    Rz_beta = np.array([[np.cos(beta), -np.sin(beta), 0],
                        [np.sin(beta), np.cos(beta), 0],
                        [0, 0, 1]])
    
    return dRz_phi @ Ry_theta @ Rz_beta

def partial_R_theta(phi, theta, beta):
    Rz_phi = np.array([[np.cos(phi), -np.sin(phi), 0],
                       [np.sin(phi), np.cos(phi), 0],
                       [0, 0, 1]])
    
    dRy_theta = np.array([[-np.sin(theta), 0, np.cos(theta)],
                          [0, 0, 0],
                          [-np.cos(theta), 0, -np.sin(theta)]])
    
    Rz_beta = np.array([[np.cos(beta), -np.sin(beta), 0],
                        [np.sin(beta), np.cos(beta), 0],
                        [0, 0, 1]])
    
    return Rz_phi @ dRy_theta @ Rz_beta

def partial_R_beta(phi, theta, beta):
    Rz_phi = np.array([[np.cos(phi), -np.sin(phi), 0],
                       [np.sin(phi), np.cos(phi), 0],
                       [0, 0, 1]])
    
    Ry_theta = np.array([[np.cos(theta), 0, np.sin(theta)],
                         [0, 1, 0],
                         [-np.sin(theta), 0, np.cos(theta)]])
    
    dRz_beta = np.array([[-np.sin(beta), -np.cos(beta), 0],
                         [np.cos(beta), -np.sin(beta), 0],
                         [0, 0, 0]])
    
    return Rz_phi @ Ry_theta @ dRz_beta

def compute_p0(R, V, u):
    lhs = np.eye(3)
    rhs = np.zeros(3)
    for i in range(len(V)):
        lhs += np.eye(3) - np.outer(u[i], u[i])
        rhs += V[i] - R @ u[i]
    return np.linalg.solve(lhs, rhs)

def newton_raphson_multi(phi_init, theta_init, beta_init, V, u, tol=1e-6, max_iter=100):
    phi = phi_init
    theta = theta_init
    beta = beta_init
    
    for _ in range(max_iter):
        R = compute_R(phi, theta, beta)
        p0 = compute_p0(R, V, u)
        F = np.zeros(3)
        J = np.zeros((3, 3))
        
        for i in range(len(V)):
            F += R @ u[i] + p0 - V[i]
            J += partial_R_phi(phi, theta, beta) @ u[i]
            J += partial_R_theta(phi, theta, beta) @ u[i]
            J += partial_R_beta(phi, theta, beta) @ u[i]
        
        if np.linalg.norm(F) < tol:
            break
        
        delta = np.linalg.solve(J, -F)
        phi += delta[0]
        theta += delta[1]
        beta += delta[2]
    
    return phi, theta, beta
