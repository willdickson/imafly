import sys
import h5py
import matplotlib.pyplot as plt

def plot_data(data_file):
    # Load data from data file
    data = h5py.File(data_file, 'r')
    t = data['t'][()]
    v_stimulus = data['v_stimulus'][()]
    v_plant = data['v_plant'][()]
    v_error = data['v_error'][()]
    is_trial = data['is_trial']
    stimulus_count = data['stimulus_count']
    stimulus_event = data['stimulus_event']

    try:
        cycle_count = data['cycle_count']
        have_cycle_count = True
    except KeyError:
        have_cycle_count = False
        
    try:
        cycle_event = data['cycle_event']
        have_cycle_event = True
    except KeyError:
        have_cycle_event = False
    
    # Plot data
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

