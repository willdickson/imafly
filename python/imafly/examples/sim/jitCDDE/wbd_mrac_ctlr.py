
import numpy as np
import matplotlib.pyplot as plt
from jitcdde import jitcdde, y, t
from jitcxde_common import conditional
from symengine import sin, tanh, Abs, Max

tau = 0.250
kc = np.exp(-1)/tau
gamma = 0.0004
k_ref = 0.7*kc

ki = 0.001
kj_0 = 0.5*kc/ki
kj_1 = 2.0*kc/ki
period = 20.0
step_start = 2*period
k_change = 12.0*period
duration = 40*period
dt = 0.02
num_step = int(duration/dt)
t_array = np.linspace(tau, tau+duration, num_step) 

stim_type = 'step'

r_array = np.zeros(t_array.shape)
r_shift_array = np.zeros(t_array.shape)
kj_array = np.zeros(t_array.shape)
for i,t_val in enumerate(t_array):
    t_shift = t_val - tau
    t_shift_2x = t_val - 2*tau
    s = sin(2*np.pi*t_shift/period)
    s_shift = sin(2*np.pi*t_shift_2x/period)
    if stim_type == 'step':
        r = conditional(t_shift, step_start, 0.0, conditional(s,0.0,-1.0, 1.0))
        r_shift = conditional(t_shift_2x, step_start, 0.0, conditional(s_shift,0.0,-1.0, 1.0))
    elif stim_type == 'sin':
        r = conditional(t_shift, step_start, 0.0, s)
        r_shift = conditional(t_shift_2x, step_start, 0.0, s_shift)
    else:
        raise ValueError(f'unknown stim_type {stim_type}')
    r_array[i] = r
    r_shift_array[i] = r_shift
    kj_array[i] = conditional(t_shift, k_change, kj_0, kj_1)

kj = conditional(t-tau, k_change, kj_0, kj_1)

t_shift = t - 2*tau # 2*tau because [0,tau] is initial cond. 
s = sin(2*np.pi*(t_shift)/period)
if stim_type == 'step':
    r = conditional(t_shift, step_start, 0.0, conditional(s,0.0,-1.0, 1.0))
elif stim_type == 'sin':
    r = conditional(t_shift, step_start, 0.0, s)
else:
    raise ValueError(f'unknown stim_type {stim_type}')

# Lyapunov method
f = [ -gamma*(y(2,t) - y(1,t))*(r - y(1,t-tau)), k_ref*(r - y(1,t - tau)), y(0,t)*kj*(r - y(2, t - tau)) ]

# MIT rule (crappy)
#f = [ -gamma*(y(2,t) - y(1,t))*y(1,t), k_ref*(r - y(1,t - tau)), y(0,t)*kj*(r - y(2, t - tau)) ]
#f = [ -gamma*(y(2,t) - y(1,t))*conditional(y(1,t), 0.0, -1.0, 1.0), k_ref*(r - y(1,t - tau)), y(0,t)*kj*(r - y(2, t - tau)) ]
DDE = jitcdde(f)
DDE.constant_past([0.8*ki, 0.0,0.0])
DDE.adjust_diff()

y_array = np.zeros((t_array.shape[0],3))

for i, t_val in enumerate(t_array):
    y_array[i,:] = DDE.integrate(t_val)
    print(t_val, y_array[i,2])

t_array = t_array - tau
fig1, ax1 = plt.subplots(4,1,sharex=True)

ax1[0].plot(t_array, r_array, 'r')
ax1[0].plot(t_array, y_array[:,2], 'b')
ax1[0].set_ylabel('v (px/sec)')
ax1[0].grid(True)

#ax1[1].plot(t_array, y_array[:,0]*kj_array, 'b')
#ax1[1].set_ylabel('ki*kj')
ax1[1].plot(t_array, y_array[:,0], 'b')
ax1[1].set_ylabel('ki')
ax1[1].grid(True)

ax1[2].plot(t_array, r_array, 'r')
ax1[2].plot(t_array, y_array[:,1], 'b')
ax1[2].set_ylabel('vm (px/sec)')
ax1[2].grid(True)

#dki = -gamma*(y_array[:,2] - y_array[:,1])*y_array[:,1]
dki = -gamma*(y_array[:,2] - y_array[:,1])*(r_shift_array - y_array[:,2])
ax1[3].plot(t_array, dki, 'b')
ax1[3].set_ylabel('dtheta/dt')
ax1[3].grid(True)

ax1[3].set_xlabel('t (sec)')
print(k_ref)

#fig2, ax2 = plt.subplot(2,1, sharex=True)
#ax2[0].plot(t_array, 
plt.show()


