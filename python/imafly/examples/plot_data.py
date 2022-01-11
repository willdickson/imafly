import sys
import h5py
import matplotlib.pyplot as plt

def plot_data(data_file):
    # Load data from data file
    data = h5py.File(data_file, 'r')
    t = data['t'][()]
    v_stimulus = data['v_stimulus'][()]
    v_plant = data['v_plant'][()]
    
    # Plot data
    fig, ax = plt.subplots(1,1)
    ax.plot(t, v_stimulus[:,0],'b')
    ax.plot(t, v_plant[:,0],'r')
    ax.set_xlabel('t (sec)')
    ax.set_ylabel('velocity (pix/sec)')
    ax.grid(True)
    plt.show()


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    plot_data(sys.argv[1])

