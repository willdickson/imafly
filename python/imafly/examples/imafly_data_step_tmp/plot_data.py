import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.interpolate as interp

filename = sys.argv[1]


data = h5py.File(filename, 'r')
for k in data:
    print(k)

t = data['t'][()]
vp = data['v_plant'][()]
vs = data['v_stimulus'][()]
ve = data['v_error'][()]
is_trial = data['is_trial'][()]
count = data['stimulus_count'][()]

tau = 0.280

mask = is_trial > 0
t = t[mask]
vp = vp[mask][:,0]
vs = vs[mask][:,0]
ve = ve[mask][:,0]
count = count[mask]
dt = t[1] - t[0]

count_values = np.unique(count)
print(count_values)


t_shift = t - tau
ve_func = interp.interp1d(t,ve,kind='linear',bounds_error=False)
ve_shift = ve_func(t_shift)

window = 21
order = 3
vp_filt = sig.savgol_filter(vp, window, order, 0)
dvp_filt = sig.savgol_filter(vp, window, order, 1)/dt

fig1, ax1 = plt.subplots(4,1,sharex=True)
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
ax1[n].plot(t, ve, 'b')
#ax1[n].plot(t, ve, 'r')
ax1[n].grid(True)
ax1[n].set_ylabel(r'$e(t-\tau)$ $(pix/sec)$')

n+=1
ax1[n].plot(t, count, 'b')
ax1[n].grid(True)
ax1[n].set_ylabel('count')
ax1[n].set_xlabel(r'$t$ $(sec)$')


fig2, ax2 = plt.subplots(1,1)
ax2.plot(ve_shift, dvp_filt/800.0, '.')
ax2.grid(True)
ax2.set_xlabel(r'$e(t-\tau)$')
ax2.set_ylabel(r'$\dot{u}(t)$')

plt.show()






