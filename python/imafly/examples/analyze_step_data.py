import sys
import json
import h5py
import numpy as np
import matplotlib.pyplot as plt
import sys_id_utils


for i, data_file in enumerate(sys.argv[1:]):


    data = h5py.File(data_file, 'r')
    run_param = json.loads(data.attrs['jsonparam'])
    print(run_param)
    t = data['t'][()]
    v_stimu = data['v_stimulus'][()]
    v_plant = data['v_plant'][()]
    v_error = data['v_error'][()]
    is_trial = data['is_trial'][()]
    stimu_count = data['stimulus_count'][()]
    stimu_event = data['stimulus_event'][()]
    
    # Mask of trial region
    mask = is_trial > 0
    t = t[mask]
    v_stimu = v_stimu[mask]
    v_plant = v_plant[mask]
    v_error = v_error[mask]
    stimu_count = stimu_count[mask]
    stimu_event = stimu_event[mask]
    
    
    # Remove last few points
    k = 3
    t = t[:-k]
    v_stimu = v_stimu[:-k]
    v_plant = v_plant[:-k]
    v_error = v_error[:-k]
    stimu_count = stimu_count[:-k]
    stimu_event = stimu_event[:-k]
    
    num_pts = t.shape[0]
    nperseg = num_pts/13
    f_sample = 1.0/(t[1] - t[0])
    f_cutoff = 0.7 
    
    # Compute gain and phase as funtion of frequency
    f, gain_db, phase_deg = sys_id_utils.freq_response(v_stimu[:,0], v_plant[:,0], f_sample, f_cutoff, nperseg)
    
    if i==0:
        fig0, ax0 = plt.subplots(3,1,sharex=True)
    ax0[0].plot(t, v_stimu[:,0],'b')
    ax0[0].plot(t, v_plant[:,0],'r')
    ax0[0].set_ylabel('vel (pix/sec)')
    ax0[0].grid(True)
    
    ax0[1].plot(t, v_error[:,0],'b')
    ax0[1].grid(True)
    ax0[1].set_ylabel('err (pix/sec)')
    
    ax0[2].plot(t, stimu_count)
    ax0[2].grid(True)
    ax0[2].set_xlabel('t (sec)')
    
    if i==0:
        fig1, ax1 = plt.subplots(2,1,sharex=True)
    fig1.suptitle('Frequency Response')
    ax1[0].semilogx(f, gain_db,'or')
    ax1[0].grid(True, which='both', axis='both')
    ax1[0].set_ylabel('gain (dB)')
    ax1[1].semilogx(f, phase_deg,'or')
    ax1[1].grid(True, which='both', axis='both')
    ax1[1].set_ylabel('phase lag (deg)')
    ax1[1].set_xlabel('f (Hz)')


plt.show()


#tau = 0.28
#f_delay = np.linspace(0.05, f.max(), 1000)
#omega_delay = 2.0*np.pi*f_delay
#tf_delay = np.exp(-1.0j*omega_delay*tau)
#gain_delay = np.absolute(tf_delay)
#gain_delay_db = 20.0*np.log10(gain_delay)
#phase_delay = np.arctan2(np.imag(tf_delay), np.real(tf_delay))
#phase_delay_deg = np.rad2deg(phase_delay)
