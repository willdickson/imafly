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
                'type'        : 'step',
                'amplitude'   : 400.0,
                'period'      : 20.0,
                't_settle'    : 10.0,
                'max_count'   : 10,
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
                'ygain' : 0,
                },
            },
        'time_step' : 0.02,
        }

kj = 2000

param['plant']['model']['xgain'] = kj
param['data_file'] = f'data_kj_{kj}.hdf5'
test = imafly.TrialRunner(param)
test.run()
plot_data(param['data_file'])

