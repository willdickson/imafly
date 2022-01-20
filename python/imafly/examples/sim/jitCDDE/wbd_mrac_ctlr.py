
import numpy as np
import matplotlib.pyplot as plt
from jitcdde import jitcdde, y, t
from jitcxde_common import conditional
from symengine import sin, tanh, Abs, Max

tau = 0.250
kc = np.exp(-1)/tau
gamma = 0.0004
k_ref = 0.5*kc

ki = 0.001
kj_0 = 0.5*kc/ki
kj_1 = 2.5*kc/ki
period = 20.0
step_start = 2*period
k_change = 12.0*period
duration = 40*period
dt = 0.02
num_step = int(duration/dt)
t_array = np.linspace(tau, tau+duration, num_step) 

r_array = np.zeros(t_array.shape)
kj_array = np.zeros(t_array.shape)
for i,t_val in enumerate(t_array):
    t_shift = t_val - tau
    s = sin(2*np.pi*(t_shift)/period)
    r = conditional(t_shift, step_start, 0.0, conditional(s,0.0,-1.0, 1.0))
    #r = conditional(t_shift, step_start, 0.0, s)
    r_array[i] = r
    kj_array[i] = conditional(t_shift, k_change, kj_0, kj_1)

kj = conditional(t-tau, k_change, kj_0, kj_1)

t_shift = t - 2*tau
s = sin(2*np.pi*(t_shift)/period)
r = conditional(t_shift, step_start, 0.0, conditional(s,0.0,-1.0, 1.0))
#r = conditional(t_shift, step_start, 0.0, s)

f = [ -gamma*(y(2,t) - y(1,t))*y(1,t), k_ref*(r - y(1,t - tau)), y(0,t)*kj*(r - y(2, t - tau)) ]
#f = [ -gamma*(y(2,t) - y(1,t))*conditional(y(1,t), 0.0, -1.0, 1.0), k_ref*(r - y(1,t - tau)), y(0,t)*kj*(r - y(2, t - tau)) ]
DDE = jitcdde(f)
DDE.constant_past([0.8*ki, 0.0,0.0])
DDE.adjust_diff()

y_array = np.zeros((t_array.shape[0],3))

for i, t_val in enumerate(t_array):
    y_array[i,:] = DDE.integrate(t_val)
    print(t_val, y_array[i,2])

t_array = t_array - tau
fig, ax = plt.subplots(4,1,sharex=True)

ax[0].plot(t_array, r_array, 'r')
ax[0].plot(t_array, y_array[:,2], 'b')
ax[0].set_ylabel('v (px/sec)')
ax[0].grid(True)

ax[1].plot(t_array, y_array[:,0]*kj_array, 'b')
ax[1].set_ylabel('ki*kj')
ax[1].grid(True)

ax[2].plot(t_array, r_array, 'r')
ax[2].plot(t_array, y_array[:,1], 'b')
ax[2].set_ylabel('vm (px/sec)')
ax[2].grid(True)

dki = -gamma*(y_array[:,2] - y_array[:,1])*y_array[:,1]
ax[3].plot(t_array, dki, 'b')
ax[3].set_ylabel('dtheta/dt')
ax[3].grid(True)

ax[3].set_xlabel('t (sec)')
print(k_ref)
plt.show()


