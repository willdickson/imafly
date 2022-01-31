import sys
import h5py
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def plot_data(data_file):
    # Load data from data file
    data = h5py.File(data_file, 'r')
    t = data['t'][()]
    v_stimulus = data['v_stimulus'][()]
    v_plant = data['v_plant'][()]
    v_error = data['v_error'][()]
    is_trial = data['is_trial'][()]
    stimulus_count = data['stimulus_count'][()]
    stimulus_event = data['stimulus_event'][()]

    try:
        cycle_count = data['cycle_count'][()]
        have_cycle_count = True
    except KeyError:
        have_cycle_count = False
        
    try:
        cycle_event = data['cycle_event'][()]
        have_cycle_event = True
    except KeyError:
        have_cycle_event = False

    mask = np.logical_and(stimulus_count >= 6, stimulus_count <=9)
    t = t[mask]
    v_stimulus = v_stimulus[mask,:]
    v_plant = v_plant[mask,:]
    v_error = v_error[mask,:]


    if 0:
        fig, ax = plt.subplots(2,1,sharex=True)
        n = 0
        ax[n].plot(t, v_stimulus[:,0],'b')
        ax[n].plot(t, v_plant[:,0],'r')
        ax[n].set_ylabel('vel (pix/sec)')
        ax[n].grid(True)

        n += 1
        ax[n].plot(t, v_error[:,0],'b')
        ax[n].grid(True)
        ax[n].set_ylabel('err (pix/sec)')
        ax[n].set_xlabel('t (sec)')

    if 1:
        fig, ax = plt.subplots(1,1,sharex=True,figsize=(8,5))
        h_stimulus, = ax.plot(t, v_stimulus[:,0],'k',linewidth=2)
        h_plant, = ax.plot(t, v_plant[:,0],'b', linewidth=2)
        ax.set_ylabel('v (pix/sec)', fontsize=14)
        ax.set_xlabel('t (sec)', fontsize=14)
        ax.grid(True)
        rect = ax.add_patch(matplotlib.patches.Rectangle((158, 330), 4, 90, linewidth=2, edgecolor='r', facecolor='none'))
        fig.legend((h_stimulus, h_plant), ('r(t)', 'v(t)'), 'best', fontsize=14)
        fig.tight_layout()
        fig.savefig('step_response.png') 



    
    if 0:
        num_plots = 5
        if have_cycle_count and have_cycle_event:
            num_plots = 7
        fig, ax = plt.subplots(num_plots,1,sharex=True)
        n = 0
        ax[n].plot(t, v_stimulus[:,0],'b')
        ax[n].plot(t, v_plant[:,0],'r')
        ax[n].set_xlabel('t (sec)')
        ax[n].set_ylabel('velocity (pix/sec)')
        ax[n].grid(True)

        n += 1
        ax[n].plot(t, v_error[:,0],'b')
        ax[n].grid(True)

        n += 1
        ax[n].plot(t, is_trial,'b')
        ax[n].grid(True)

        n += 1
        ax[n].plot(t,stimulus_count)
        ax[n].grid(True)

        if have_cycle_count:
            n += 1
            ax[n].plot(t,cycle_count)
            ax[n].grid(True)

        n += 1
        ax[n].plot(t,stimulus_event)
        ax[n].grid(True)

        if have_cycle_event:
            n += 1
            ax[n].plot(t,cycle_event)
            ax[n].grid(True)

    plt.show()


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    plot_data(sys.argv[1])

