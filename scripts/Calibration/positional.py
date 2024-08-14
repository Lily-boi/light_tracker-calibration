import numpy as np
import math




'''
Functions for ease of use
'''
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm
def out(target, val, val2 = None):
    opt = op(target)
    opt.par.value0 = val[0]
    opt.par.value1 = val[1]
    opt.par.value2 = val[2]
    if val2:
        opt.par.value3 = val2[0]
        opt.par.value4 = val2[1]
        opt.par.value5 = val2[2]       
def out_par(target, val):
    for i, t in enumerate(['x', 'y', 'z']):
        print(f'parent().par.{target}{t} = {val[i][0]}')
        exec(f'parent().par.{target}{t} = {val[i][0]}')        
def ATV(pt):
    pan, tilt = pt
    ct = math.cos(tilt)
    st = math.sin(tilt)
    cp = math.cos(pan) 
    sp = math.sin(pan)
    return [ct*cp, st, ct*sp]
    

def onSetupParameters(scriptOp):
    page = scriptOp.appendCustomPage('Custom')
    p = page.appendPulse('Calibrate', label='Calibrate')
   
    return

def onPulse(par):
    data = op('cal')
        
    def data_get(row, cols, cole=0):
        cole = cole or cols + 2
        sample = []
        for i in range(cols, cole+1):
            sample.append(float(data[row, i]))
        return sample
    
    if par:
        V = []
        u = []
        for i in range(4, data.numRows):
            if int(data_get(i, 5, 5)[0]) == 1:
                v_ = data_get(i, 0)
                u_ = ATV(data_get(i, 3, 4))
                V.append(v_)
                u.append(u_)
                out(f'vect{i}', u_, v_)
                print(f'vect {i}: {u_}, {v_}')
            
        V = np.array(V)
        u = np.array(u)

        phi_init = 0.0
        theta_init = 0.0
        beta_init = 0.0

        phi_opt, theta_opt, beta_opt = newton_raphson_multi(phi_init, theta_init, beta_init, V, u)

        print(f"Optimal phi: {phi_opt}\ntheta: {theta_opt}\nbeta: {beta_opt}")
        
        p0 = compute_p0(compute_R(phi_opt, theta_opt, beta_opt), V, u)
        r = compute_R(phi_opt, theta_opt, beta_opt)
        
        print(f'Optimal p0: {p0} \nR: {r}')
        
        up = np.array(op('par').numpyArray()[1:4])
        up = normalize(r @ up)
        print(f'Up: {up}')
        resting = np.array(op('par').numpyArray()[4:7])
        resting = normalize(r @ resting)
        print(f'Resting: {resting}')
        
        out_par('Mountedplane', up)
        out_par('Resting', resting)
        out_par('Position', [[x] for x in p0])
        
        for n, i in enumerate(u):
            i = r @ i
            n = n+3
            op(f'vect{n+1}').par.value6 = i[0]
            op(f'vect{n+1}').par.value7 = i[1]
            op(f'vect{n+1}').par.value8 = i[2]
        
        
def onCook(scriptOp):
    scriptOp.clear()
    return

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

def objective_functions(phi, theta, beta, V, u):
    N = V.shape[0]
    R = compute_R(phi, theta, beta)
    p0 = compute_p0(R, V, u)
    
    f1 = f2 = f3 = 0
    for i in range(N):
        Vi_minus_p0 = V[i] - p0
        I_minus_uuT = np.eye(3) - np.outer(u[i], u[i])
        RT_Vi_minus_p0 = R.T @ Vi_minus_p0
        
        f1 += Vi_minus_p0.T @ partial_R_phi(phi, theta, beta) @ I_minus_uuT @ RT_Vi_minus_p0
        f2 += Vi_minus_p0.T @ partial_R_theta(phi, theta, beta) @ I_minus_uuT @ RT_Vi_minus_p0
        f3 += Vi_minus_p0.T @ partial_R_beta(phi, theta, beta) @ I_minus_uuT @ RT_Vi_minus_p0
    
    return np.array([f1, f2, f3])

def compute_p0(R, V, u):
    N = V.shape[0]
    sum_matrix = np.zeros((3, 3))
    sum_vector = np.zeros(3)
    
    for i in range(N):
        I_minus_uuT = np.eye(3) - np.outer(u[i], u[i])
        RT_Vi = R.T @ V[i]
        
        sum_matrix += I_minus_uuT
        sum_vector += I_minus_uuT @ RT_Vi
    
    p0 = R @ np.linalg.inv(sum_matrix) @ sum_vector
    return p0

def jacobian(phi, theta, beta, V, u):
    eps = 1
    f0 = objective_functions(phi, theta, beta, V, u)
    
    J = np.zeros((3, 3))
    for i, var in enumerate([phi, theta, beta]):
        var_eps = np.copy([phi, theta, beta])
        var_eps[i] += eps
        f_eps = objective_functions(var_eps[0], var_eps[1], var_eps[2], V, u)
        print(f_eps)
        print(f0)
        J[:, i] = (f_eps - f0) / eps
    
    return J

def newton_raphson_multi(phi, theta, beta, V, u, tol=1e-15, max_iter=2):
    for i in range(max_iter):
        f = objective_functions(phi, theta, beta, V, u)
        J = jacobian(phi, theta, beta, V, u)
        try:
            delta = np.linalg.solve(J, -f)
        except:
            print(i)
            print(f'J: {J}')
            print('----')
            print(f'F: {-f}')    
        phi, theta, beta = phi + delta[0], theta + delta[1], beta + delta[2]
        
        if np.linalg.norm(delta) < tol:
            print('tol')
            break
    
    return phi, theta, beta

