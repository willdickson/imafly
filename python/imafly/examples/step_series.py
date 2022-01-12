import imafly
import h5py
import matplotlib.pyplot as plt
from plot_data import plot_data

param = {
        'stimulus': { 
            'image': {
                'type'   : 'vstripe',
                'number' : 5,
                'width'  : 800,
                'height' : 600,
                'color0' : (0,0,0),
                'color1' : (0,255,0), 
                }, 
            'motion' : {
                'type'        : 'step_series',
                'amplitude'   : 400.0,
                'period'      : 2.0,
                't_settle'    : 1.0,
                'cycles'      : 2, 
                'repetitions' : 2,
                },
            },
        'plant': {
            'input' : {
                'type'      : 'teensy',
                'port'      : '/dev/ttyACM0',
                'min_value' : 0.0,
                'max_value' : 3.3,
                },
            'model': {
                'type'  : 'velocity',
                'xgain' : 800,
                'ygain' : 0,
                },
            },
        'data_file' : 'data.hdf5', 
        'time_step' : 0.02,
        }

test = imafly.TrialRunner(param)
test.run()
plot_data(param['data_file'])

