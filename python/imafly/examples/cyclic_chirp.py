import imafly.ref_input
import numpy as np
import matplotlib.pyplot as plt

param = {
        'amplitude'  : 400.0,
        'min_freq'   : 1/60.0, 
        'max_freq'   : 1/1.0, 
        'n_cycles'   : 10,  
        't_settle'   : 10.0,
        'method'     : 'logarithmic',
        }

motion_model = imafly.ref_input.CyclicChirp(param)
print('fmin', motion_model.min_freq)
print('fmax', motion_model.max_freq)
print('tmax', 1/motion_model.min_freq)
print('tmin', 1/motion_model.max_freq)
print('T/2 ', motion_model.period/2)
print('T   ', motion_model.period)

#assert 1==0

t = np.linspace(0.0,2*motion_model.period, 2000)
vel = [motion_model.velocity(item) for item in t]
vx = [v[0] for v in vel]

fig, ax = plt.subplots(1,1,sharex=True)
ax.plot(t, vx)
ax.grid(True)
ax.set_xlabel('t (sec)')
ax.set_ylabel('value')
ax.set_title('cyclic chirp')
plt.show()
