
import numpy as np
import matplotlib.pyplot as plt
from jitcdde import jitcdde, y, t
from jitcxde_common import conditional
from symengine import sin

tau = 0.250
kc = np.exp(-1)/tau
ki = 0.001
kj = 2.5*kc/ki 
kj_0 = 0.8*kc/ki
kj_1 = 2.0*kc/ki
period = 20.0

duration = 6*period
dt = 0.01
num_step = int(duration/dt)
t_array = np.linspace(tau, tau+duration, num_step) 

r_array = np.zeros(t_array.shape)
for i,t_val in enumerate(t_array):
    t_shift = t_val - tau
    s = sin(2*np.pi*(t_shift)/period)
    r = conditional(t_shift, 2*period, 0.0, conditional(s,0.0,-1.0, 1.0))
    r_array[i] = r

kj = conditional(t-tau, 4.0*period, kj_0, kj_1)

t_shift = t - 2*tau
s = sin(2*np.pi*(t_shift)/period)
r = conditional(t_shift, 2*period, 0.0, conditional(s,0.0,-1.0, 1.0))
f = [ ki * kj * (r- y(0,t - tau)) ]
DDE = jitcdde(f)
DDE.constant_past([0.0])
DDE.adjust_diff()

y_array = np.zeros(t_array.shape)

for i, t_val in enumerate(t_array):
    y_array[i] = float(DDE.integrate(t_val))
    print(t, y_array[i])

t_array = t_array - tau
fig, ax = plt.subplots(1,1)
ax.plot(t_array, r_array, 'r')
ax.plot(t_array, y_array, 'b')
ax.grid(True)
ax.set_xlabel('t (sec)')
ax.set_ylabel('vel (px/sec)')
plt.show()


