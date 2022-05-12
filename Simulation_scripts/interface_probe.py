import numpy as np
import matplotlib.pyplot as plt
import h5py
import time
from IPython import display

from dedalus import public as de
from dedalus.extras import flow_tools

import logging
logger = logging.getLogger(__name__)

def r(x,x0):
    return np.sqrt((x-x0)**2)

def blob(x,x0,r0,w):
    return 0.5*(1 - np.tanh((r(x,x0)-r0)/w))

def interface_width(Diff,K,g):
    Lx = 9. # mm
    nx = 256 # number of grid points

    # Create bases and domain
    x_basis = de.Fourier('x', nx, interval=(0, Lx), dealias=3/2)
    domain = de.Domain([x_basis], grid_dtype=np.float64)

    problem = de.IVP(domain, variables=['rho1','rho2','rho12'])
    problem.parameters['D0'] = Diff
    problem.parameters['K'] = K
    problem.parameters['g0'] = g


    problem.substitutions['rho_b'] = "rho1+rho2  + rho12" 
    problem.substitutions["Lap(A)"] = "dx(dx(A))"

    problem.substitutions["grow_non_lin(A,B)"] = "-A*B"

    problem.add_equation("dt(rho1) - g0*rho1 - D0*Lap(rho1) = g0*grow_non_lin(rho1,rho_b) - K*rho1*rho2")
    problem.add_equation("dt(rho2) - g0*rho2 - D0*Lap(rho2) = g0*grow_non_lin(rho2,rho_b) - K*rho1*rho2")
    problem.add_equation("dt(rho12)  = 2*K*rho1*rho2")
    ts = de.timesteppers.RK443

    solver =  problem.build_solver(ts)

    x = domain.grid(0)
    rho1 = solver.state['rho1']
    rho2 = solver.state['rho2']
    rho12 = solver.state['rho12']

    r0 = 0.75 #mm
    w = 0.15 #mm

    rho1['g'] = blob(x,2,r0,w) # 2 blobs, 5mm apart
    rho2['g'] = blob(x,7,r0,w)
    solver.stop_sim_time = 80 #minutes
    dt = 0.4*Lx/nx

    logger.info('Starting loop')
    start_time = time.time()
    while solver.ok:
        solver.step(dt)
        if solver.iteration % 50 == 0:
            logger.info('Iteration: %i, Time: %e, dt: %e' %(solver.iteration, solver.sim_time, dt))
      
    scale = 24
    rho1.set_scales(scale)
    rho2.set_scales(scale)
    rho12.set_scales(scale)
    x = domain.grid(0,scales=scale)

    int_width = np.min(x[rho1['g'] + 0.5*rho12['g'] < 0.1]) - np.max(x[rho2['g'] + 0.5*rho12['g'] < 0.1])
    return int_width