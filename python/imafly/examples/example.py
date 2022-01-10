import imafly
import h5py
import matplotlib.pyplot as plt

param = {
        'stimulus': { 
            'image': {
                # ---------------------------
                'type'   : 'vstripe',
                'number' : 5,
                'width'  : 800,
                'height' : 600,
                'color0' : (0,0,0),
                'color1' : (0,255,0), 
                # ---------------------------
                #'type'   : 'ball',
                #'width'  : 1200,
                #'height' : 800,
                #'color'  : (0,255,0), 
                #'radius' : 100,
                # --------------------------- 
                }, 
            'motion' : {
                # ------------------------------
                #'type' : 'none',
                # ------------------------------
                #'type'      : 'sin',
                #'amplitude' : 300.0,
                #'period'    : 2.5,
                #'t_settle'  : 10.0,
                # ------------------------------
                'type'      : 'step',
                'amplitude' : 400.0,
                'period'    : 20.0,
                't_settle'  : 10.0,
                # ------------------------------
                #'type'      : 'step_zero_step',
                #'amplitude' : 400.0,
                #'t_step'    : 10.0, 
                #'t_zero'    : 10.0,
                #'t_settle'  : 20.0,
                # ------------------------------
                #'type'         : 'random_step',
                #'max_velocity' :  500,
                #'min_velocity' : -500,
                #'max_duration' : 10,
                #'min_duration' : 2,
                #'t_settle'   : 10.0,
                # ------------------------------
                #'type'      : 'cyclic_chirp',
                #'amplitude' : 600.0,
                #'min_freq'  : 1/60.0, 
                #'max_freq'  : 1/1.0, 
                #'n_cycles'  : 10,  
                #'t_settle'   : 10.0,
                #'method'    : 'logarithmic'
                # ------------------------------ 
                },
            },
        'plant': {
            'input' : {
                # ------------------------------
                #'type'  : 'joystick', 
                #'xcode' : 'ABS_X',
                #'ycode' : 'ABS_Y', 
                #'ximax' : 1024,
                #'yimax' : 1024,
                # ------------------------------
                'type'      : 'teensy',
                'port'      : '/dev/ttyACM0',
                'min_value' : 0.0,
                'max_value' : 3.3,
                # ------------------------------
                },
            'model': {
                # -----------------------------
                'type'  : 'velocity',
                'xgain' : 800,
                'ygain' : 0,
                # -----------------------------
                #'type'  : 'integral',
                #'xgain' : 8000,
                #'ygain' : 0,
                #'xdamp' : 0.1,
                #'ydamp' : 0,
                # -----------------------------
                },
            },
        'data_file' : 'data.hdf5', 
        'time_step' : 0.02,
        }


test = imafly.TrialRunner(param)
test.run()

# Load data from data file
data = h5py.File(param['data_file'], 'r')
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

