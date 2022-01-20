import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.interpolate as interp


file_list = ['data_step_kp800.hdf5', 'data_step_kp1600.hdf5']
color_list = ['b', 'g']
kj_list = [800.0, 1600.0]
is_first = True
tau = 0.280

for filename, color, kj in zip(file_list, color_list, kj_list):

    data = h5py.File(filename, 'r')
    
    t = data['t'][()]
    vp = data['v_plant'][()]
    vs = data['v_stimulus'][()]
    ve = data['v_error'][()]
    is_trial = data['is_trial'][()]
    
    
    mask = is_trial > 0
    t = t[mask]
    vp = vp[mask][:,0]
    vs = vs[mask][:,0]
    ve = ve[mask][:,0]
    dt = t[1] - t[0]
    
    t_shift = t - tau
    ve_func = interp.interp1d(t,ve,kind='linear',bounds_error=False)
    ve_shift = ve_func(t_shift)
    
    
    window = 21
    order = 3
    vp_filt = sig.savgol_filter(vp, window, order, 0)
    dvp_filt = sig.savgol_filter(vp, window, order, 1)/dt
    
    
    if 0:
        if is_first:
            fig1, ax1 = plt.subplots(3,1,sharex=True)
        n = 0
        ax1[n].plot(t, vs, 'r')
        ax1[n].plot(t, vp, 'b')
        ax1[n].plot(t, vp_filt, 'g')
        ax1[n].grid(True)
        ax1[n].set_ylabel('v (pix/sec)')
        
        n+=1
        ax1[n].plot(t, dvp_filt, 'b')
        ax1[n].grid(True)
        ax1[n].set_ylabel(r'$\dot{v}(t)$ $(pix/sec^2)$')
        ax1[n].set_xlabel(r'$t$ $(sec)$')
        
        n+=1
        ax1[n].plot(t, ve_shift/800.0, 'b')
        #ax1[n].plot(t, ve, 'r')
        ax1[n].grid(True)
        ax1[n].set_ylabel(r'$e(t-\tau)$ $(pix/sec)$')
        ax1[n].set_xlabel(r'$t$ $(sec)$')
    
    
    if is_first:
        fig2, ax2 = plt.subplots(1,1)
    ax2.plot(ve_shift, dvp_filt/kj, f'.{color}')
    ax2.grid(True)
    ax2.set_xlabel(r'$e(t-\tau)$')
    ax2.set_ylabel(r'$\dot{v}(t)$')

    is_first = False

plt.show()






