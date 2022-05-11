#!/usr/bin/env python
# coding: utf-8

# This script runs simulations at different seeding ratios and saves an image of the final time point in a separate folder 
# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import h5py
import time
from IPython import display
import os


from dedalus import public as de
from dedalus.extras import flow_tools

import logging
logger = logging.getLogger(__name__)

kvals = np.linspace(0,5,15)
for k in kvals:
    f_name = 'Diff_seed_{:.0f}_r'.format(100*k)
    Lx, Ly = (35, 25)
    nx, ny = (400, 400)

    # Create bases and domain
    x_basis = de.Fourier('x', nx, interval=(0, Lx), dealias=3/2)
    y_basis = de.Fourier('y', ny, interval=(0, Ly), dealias=3/2)
    domain = de.Domain([x_basis, y_basis], grid_dtype=np.float64)

    def grow_fun(A,B):
        F = (A.data)*(1-B.data)
        F[A.data < 1e-3] = 0
        return F


    def grow_operator(field1,field2):
        return de.operators.GeneralFunction(
            field1.domain,
            layout = 'g',
            func = grow_fun,
            args = (field1,field2,)
        )

    de.operators.parseables['grow'] = grow_operator


    params = np.load('Parameters.npz')
    Diff = params['Diff'].flat[0]
    K =  params['K'].flat[0]
    g = params['g'].flat[0]
    problem = de.IVP(domain, variables=['rho1','rho2','rho12'])
    problem.parameters['D0'] = Diff
    problem.parameters['K'] = K
    problem.parameters['g1'] = g
    problem.parameters['g2'] = g


    problem.substitutions['rho_b'] = "rho1+rho2+rho12"
    problem.substitutions["Lap(A)"] = "dx(dx(A)) + dy(dy(A))"


    problem.add_equation("dt(rho1)  - D0*Lap(rho1) = g1*grow(rho1,rho_b)  - K*rho1*rho2")
    problem.add_equation("dt(rho2)  - D0*Lap(rho2) = g2*grow(rho2,rho_b)  - K*rho1*rho2")
    problem.add_equation("dt(rho12)  = 2*K*rho1*rho2")

    ts = de.timesteppers.RK443

    solver =  problem.build_solver(ts)


    x = domain.grid(0)
    y = domain.grid(1)
    rho1 = solver.state['rho1']
    rho2 = solver.state['rho2']

    def r(x,y,x0,y0):
        return np.sqrt((x-x0)**2+(y-y0)**2)

    def blob(x,y,x0,y0,r0,w):
        return 0.5*(1 - np.tanh((r(x,y,x0,y0)-r0)/w))

    r0 = 0.75
    w = 0.22

    rho1['g'] = blob(x,y,Lx*0.5 - 4.5,0.5*Ly,k*1.25+r0,w)
    rho2['g'] = blob(x,y,Lx*0.5 + 4.5,0.5*Ly,r0,w)


    solver.stop_sim_time = 500
    dt = 0.4*Lx/nx

    print(f_name)
    cwd = os.getcwd()
    folder_name = cwd + '/' + f_name
    os.mkdir(folder_name)
    analysis = solver.evaluator.add_file_handler(folder_name, sim_dt=1, max_writes=500)
    analysis.add_task('rho1')
    analysis.add_task('rho2')
    analysis.add_task('rho12')


    logger.info('Starting loop')
    start_time = time.time()
    while solver.ok:
        solver.step(dt)
        if solver.iteration % 50 == 0:
            logger.info('Iteration: %i, Time: %e, dt: %e' %(solver.iteration, solver.sim_time, dt))



    from dedalus.tools import post
    post.merge_process_files(f_name, cleanup=True)


    # In[14]:


    f = h5py.File(f_name + '/' + f_name + '_s1.h5','r')
    y = f['/scales/y/1.0'][:]
    x = f['/scales/x/1.0'][:]
    t = f['scales']['sim_time'][:]
    rho1 = f['tasks']['rho1'][:]
    rho2 = f['tasks']['rho2'][:]
    rhom = f['tasks']['rho12'][:]

    rho_t = rho1+ rho2+rhom

    xm, ym = np.meshgrid(x,y)
    fig, axis = plt.subplots(1,1,figsize=(12,6))

    i = -1

    p = axis.pcolormesh(xm, ym,  (rho_t[i,:,:]).T, cmap='Greys_r', vmin=0.6, vmax=1.08);
    axis.set_xlim([0,Lx])
    axis.set_ylim([0,Ly])
    axis.set_aspect('equal')
    fig.savefig(f_name + '.png')
