import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.interpolate as interp

filename = sys.argv[1]

tau = 0.280
filt_window = 21
filt_order = 3
grab_dt_frac = 0.1
grab_ve_thresh = 0.99
kj = 800.0

data = h5py.File(filename, 'r')
#for k in data:
#    print(k)

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
dt = t[1] - t[0]

vs_max = vs.max()
vs_min = vs.min()

t_shift = t - tau
ve_func = interp.interp1d(t,ve,kind='linear',bounds_error=False)
ve_shift = ve_func(t_shift)

vp_filt = sig.savgol_filter(vp, filt_window, filt_order, 0)
dvp_filt = sig.savgol_filter(vp, filt_window, filt_order, 1, delta=dt)

count_to_data = {}
for count in np.unique(step_count):
    count_mask = step_count == count 
    count_to_data[count] = {
            't'        : t[count_mask],
            'vp'       : vp[count_mask],
            'vs'       : vs[count_mask],
            've'       : ve[count_mask],
            't_shift'  : t_shift[count_mask],
            've_shift' : ve_shift[count_mask],
            'dvp_filt' : dvp_filt[count_mask],
            }



count_to_pos_data = {}
count_to_neg_data = {}
for count, data_dict in count_to_data.items():
    tt = data_dict['t']
    t0 = data_dict['t'][0]
    t1 = data_dict['t'][-1]
    grab_dt = grab_dt_frac*(t1-t0)
    mask = np.logical_and(tt - t0 > tau, tt < t0 + grab_dt)
    mask = np.logical_and(mask, data_dict['ve_shift'] < grab_ve_thresh*data_dict['ve_shift'].max())
    count_to_pos_data[count] = {
            't'        : tt[mask], 
            'vp'       : data_dict['vp'][mask],
            'vs'       : data_dict['vs'][mask],
            've'       : data_dict['ve'][mask],
            't_shift'  : data_dict['t_shift'][mask],
            've_shift' : data_dict['ve_shift'][mask],
            'dvp_filt' : data_dict['dvp_filt'][mask], 
            }

    t0 = data_dict['t'][0] + 0.5*(t1 - t0)
    mask = np.logical_and(tt - t0 > tau, tt < t0 + grab_dt)
    mask = np.logical_and(mask, data_dict['ve_shift'] > grab_ve_thresh*data_dict['ve_shift'].min())
    count_to_neg_data[count] = {
            't'        : tt[mask], 
            'vp'       : data_dict['vp'][mask],
            'vs'       : data_dict['vs'][mask],
            've'       : data_dict['ve'][mask],
            't_shift'  : data_dict['t_shift'][mask],
            've_shift' : data_dict['ve_shift'][mask],
            'dvp_filt' : data_dict['dvp_filt'][mask], 
            }


fig1, ax1 = plt.subplots(4,1,sharex=True)
n = 0
ax1[n].plot(t, vs, 'r')
ax1[n].plot(t, vp, 'b')
ax1[n].plot(t, vp_filt, 'g')
ax1[n].grid(True)
ax1[n].set_ylabel('v (pix/sec)')

n+=1
ax1[n].plot(t, dvp_filt, 'b')
for count, data_dict in count_to_pos_data.items():
    ax1[n].plot(data_dict['t'], data_dict['dvp_filt'], 'r')
for count, data_dict in count_to_neg_data.items():
    ax1[n].plot(data_dict['t'], data_dict['dvp_filt'], 'g')
ax1[n].grid(True)
ax1[n].set_ylabel(r'$\dot{v}(t)$ $(pix/sec^2)$')
ax1[n].set_xlabel(r'$t$ $(sec)$')

n+=1
ax1[n].plot(t, ve_shift, 'b')
for count, data_dict in count_to_pos_data.items():
    ax1[n].plot(data_dict['t'], data_dict['ve_shift'], 'r')
for count, data_dict in count_to_neg_data.items():
    ax1[n].plot(data_dict['t'], data_dict['ve_shift'], 'g')
ax1[n].grid(True)
ax1[n].set_ylabel(r'$e(t-\tau)$ $(pix/sec)$')

n+=1
ax1[n].plot(t, step_count, 'b')
ax1[n].grid(True)
ax1[n].set_ylabel('step_count')
ax1[n].set_xlabel(r'$t$ $(sec)$')


#fig2, ax2 = plt.subplots(1,1)
#ax2.plot(ve_shift, dvp_filt/kj, '.')
#ax2.grid(True)
#ax2.set_xlabel(r'$e(t-\tau)$')
#ax2.set_ylabel(r'$\dot{u}(t)$')


fig3, ax3 = plt.subplots(1,1)
ve_shift_list = []
dvp_filt_list = []
for count, data_dict in count_to_pos_data.items():
    #ax3.plot(data_dict['ve_shift'], data_dict['dvp_filt'], 'b.')
    ve_shift_list.extend(data_dict['ve_shift'].tolist())
    dvp_filt_list.extend(data_dict['dvp_filt'].tolist())
for count, data_dict in count_to_neg_data.items():
    #ax3.plot(data_dict['ve_shift'], data_dict['dvp_filt'], 'b.')
    ve_shift_list.extend(data_dict['ve_shift'].tolist())
    dvp_filt_list.extend(data_dict['dvp_filt'].tolist())

ve_shift_array = np.array(ve_shift_list)
dvp_filt_array = np.array(dvp_filt_list)
du_filt_array = dvp_filt_array/kj

fit = np.polyfit(ve_shift_array, du_filt_array, 1)
ve_shift_fit = np.linspace(ve_shift_array.min(), ve_shift_array.max(), 1000)
du_filt_fit = np.polyval(fit, ve_shift_fit)
ax3.plot(ve_shift_array, du_filt_array, 'b.')
ax3.plot(ve_shift_fit, du_filt_fit, 'r', linewidth=4)
ax3.grid(True)
ax3.set_xlabel(r'$e(t-\tau)$')
ax3.set_ylabel(r'$\dot{u}(t)$')
print(fit)
print(fit[0]*kj)
plt.show()



