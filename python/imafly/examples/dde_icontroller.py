import numpy as np
import matplotlib.pyplot as plt
import ddeint
import sys_id_utils




class DelayIController:

    def __init__(self, param):
        self.param = param
        self.ref_input_func = self.get_ref_input_func()
        self.ini_cond_func = self.zero_func

    @property
    def delay(self):
        return self.param['delay']

    @property
    def gain_joy(self):
        return self.param['gain_joy']

    @property
    def gain_int(self):
        return self.param['gain_int']

    @property
    def ref_input_param(self):
        return self.param['ref_input']

    def transfer_func(self,s):
        numer = self.gain_joy*self.gain_int*np.exp(-self.delay*s)
        denom = s + self.gain_joy*self.gain_int*np.exp(-self.delay*s)
        return numer/denom

    def get_ref_input_func(self):
        if self.ref_input_param['type'] == 'zero':
            return self.zero_func
        elif self.ref_input_param['type'] == 'step':
            return self.step_func

    def zero_func(self,t):
        return 0.0

    def step_func(self,t):
        t0 = self.ref_input_param['t0']
        T = self.ref_input_param['period']
        A = self.ref_input_param['amplitude']
        val = 0.0
        if t > t0:
            t_mod_T = (t - t0) % T
            if t_mod_T <= 0.5*T:
                val = A
            else:
                val = -A
        return val

    def model(self, v, t):
        rd = self.ref_input_func(t-self.delay)
        vd = v(t - self.delay)
        ed =  rd - vd
        value = self.gain_joy*self.gain_int*ed 
        print(t)
        return value

    def run(self, t):
        v = ddeint.ddeint(self.model, self.ini_cond_func, t) 
        return np.array([float(item) for item in v])


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    param = {
            'delay'        : 0.250,
            'gain_joy'     : 1*800.0,
            'gain_int'     : 1.0*0.0015, 
            'ref_input'    : {
                'type'       : 'step',
                't0'         : 0.0,
                'period'     : 20.0,
                'amplitude'  : 300.0, 
                },
            }

    t = np.linspace(0.0, 3*20, 10000)

    dde_ctlr = DelayIController(param)
    v = dde_ctlr.run(t)
    v = np.array([float(val) for val in v])
    r = np.array([dde_ctlr.ref_input_func(val) for val in t])

    num_pts = t.shape[0]
    nperseg = num_pts/3
    f_sample = 1.0/(t[5] - t[4])
    f_cutoff =  1.0 

    # Compute gain and phase as funtion of frequency
    #f, gain_db, phase_deg = sys_id_utils.freq_response(r, v, f_sample, f_cutoff, nperseg, gain_in_db=False)
    f, gain_db, phase_deg = sys_id_utils.freq_response(r, v, f_sample, f_cutoff, nperseg) 
    print(f.max())

    f_tf = np.linspace(f.min(), f.max(), 1000)
    omegaj = 2.0*np.pi*1.0j*f_tf

    tf_at_omegaj = dde_ctlr.transfer_func(omegaj)
    gain_tf = np.absolute(tf_at_omegaj)
    gain_tf_db = 20.0*np.log10(gain_tf)
    phase_tf_rad = np.arctan2(np.imag(tf_at_omegaj), np.real(tf_at_omegaj))
    phase_tf_deg = np.rad2deg(phase_tf_rad)

    fig0, ax0 = plt.subplots(1,1)
    ax0.plot(t, r, 'r')
    ax0.plot(t, v, 'b')
    ax0.set_xlabel('t (sec)')
    ax0.set_ylabel('v')
    ax0.grid(True)


    fig1, ax1 = plt.subplots(2,1,sharex=True)
    fig1.suptitle('Frequency Response')
    ax1[0].semilogx(f_tf, gain_tf_db,'b')
    ax1[0].semilogx(f, gain_db,'or')
    ax1[0].grid(True, which='both', axis='both')
    ax1[0].set_ylabel('gain (dB)')

    ax1[1].semilogx(f_tf, phase_tf_deg,'b')
    ax1[1].semilogx(f, phase_deg,'or')
    ax1[1].grid(True, which='both', axis='both')
    ax1[1].set_ylabel('phase lag (deg)')
    ax1[1].set_xlabel('f (Hz)')

    plt.show()


