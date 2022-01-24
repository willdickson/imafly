import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.interpolate as interp

def theta_estimator(vp, ve, kj, tau, window=200, ve_threshold=0.60, savgol_filt_window=61, savgol_filt_order=3):

    num_pts = t.size
    dt = t[1] - t[0]

    # Get tau shifted velocity error
    t_shift = t - tau
    ve_func = interp.interp1d(t,ve,kind='linear',bounds_error=False,fill_value=0.0)
    ve_shift = ve_func(t_shift)

    # Get derivative of plant velocity
    vp_filt = sig.savgol_filter(vp, savgol_filt_window, savgol_filt_order, 0)
    dvp_filt = sig.savgol_filter(vp, savgol_filt_window, savgol_filt_order, 1, delta=dt)

    #plt.plot(t,vp,'b')
    #plt.plot(t,vp_filt,'r')
    #plt.show()

    # Get numerator and denominator arrays
    numer = np.zeros(num_pts)
    denom = np.zeros(num_pts)
    for i in range(window,num_pts-window):
        n = i - window
        m = i + window + 1
        numer[i] = (ve_shift[n:m]*dvp_filt[n:m]).sum()
        denom[i] = (ve_shift[n:m]**2).sum()

    # Get threshold of computing theta
    denom_threshold = ve_threshold*np.absolute(denom).max()
    numer_threshold = ve_threshold*np.absolute(numer).max()

    # Compute theta
    theta = np.zeros(num_pts)
    for i in range(window,num_pts-window):
        if np.absolute(denom[i]) < denom_threshold: # or np.absolute(numer[i]) < numer_threshold:
            theta[i] = theta[i-1]
        else:
            theta[i] = (1/kj)*numer[i]/denom[i]
            #theta[i] = numer[i]/denom[i]

    return theta






# ------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    filename = sys.argv[1]
    
    tau = 0.280
    kj = 800.0
    
    
    data = h5py.File(filename, 'r')
    
    t = data['t'][()]
    vp = data['v_plant'][()]
    vs = data['v_stimulus'][()]
    ve = data['v_error'][()]
    is_trial = data['is_trial'][()]
    step_count = data['stimulus_count'][()]
    
    mask = is_trial > 0
    t = t[mask]
    vp = vp[mask][:,0]
    vs = vs[mask][:,0]
    ve = ve[mask][:,0]
    step_count = step_count[mask]

    theta = theta_estimator(vp, ve, kj, tau)
    theta_filt = sig.savgol_filter(theta, 501, 3, 0)

    fig, ax = plt.subplots(2,1, sharex=True)
    ax[0].plot(t,vs,'b')
    ax[0].plot(t,vp, 'r')
    ax[0].grid(True)

    #ax[1].plot(t,theta,'b')
    ax[1].plot(t,theta_filt,'r')
    ax[1].set_xlabel('t (sec)')
    ax[1].set_ylabel('theta')
    ax[1].grid(True)
    plt.show()








