import numpy as np
import scipy.signal as sig

class RefInput:
    """
    Base class for reference inputs
    """

    def __init__(self, param, t_init=0.0):
        self.param = param
        self.t_init = t_init
        self._count = -1 
        self._last_count = -2 

    @property
    def event(self):
        return self._count != self._last_count

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self,value):
        self._last_count = self._count
        self._count = value

    @property
    def t_settle(self):
        try:
            t_settle = self.param['t_settle']
        except KeyError:
            t_settle = 0.0
        return t_settle

    @property
    def max_count(self):
        try:
            max_count = self.param['max_count']
        except KeyError:
            max_count = None
        return max_count

    @property
    def done(self):
        if self.max_count is not None:
            rval = self.count > self.max_count
        else:
            rval = False
        return rval 

    def t_rel(self,t):
        return t - self.t_init - self.t_settle

    def is_trial(self,t):
        return self.t_rel(t) >= 0.0

    def velocity(self,t):
        t_rel = self.t_rel(t)
        if t_rel < 0.0:
            self.count = -1
        else:
            self.count = 0
        vx = 0.0
        vy = 0.0
        return np.array([vx, vy])


class NoMotion(RefInput):

    def __init__(self, param, t_init=0.0):
        super().__init__(param, t_init=t_init)


class DoneMotion(RefInput):

    def __init__(self, param, t_init=0.0):
        super().__init__(param, t_init=t_init)

    @property
    def done(self):
        return True


class BaseSeries(RefInput):

    def __init__(self, param, t_init=0.0):
        super().__init__(param, t_init=t_init)
        self.motion = DoneMotion({}) 
        self.motion_model = DoneMotion
        self._count = 0 
        self._last_count = -1 
        self.is_first = True

    @property
    def event(self):
        #return (self._count != self._last_count) and self.motion.event
        return self._count != self._last_count

    @property
    def done(self):
        return self.count == self.repetitions 

    @property
    def repetitions(self):
        return self.param['repetitions']

    @property
    def cycles(self):
        return self.param['cycles']

    @property
    def motion_param(self):
        return {}

    def is_trial(self,t):
        return self.motion.t_rel(t) >= 0.0

    def next_motion(self,t):
        if not self.is_first:
            self.count += 1
        else:
            self.is_first = False
        if self.count < self.repetitions:
            motion = self.motion_model(self.motion_param, t_init=t)
        else:
            motion = DoneMotion({})
        return motion

    def velocity(self,t):
        vel = self.motion.velocity(t)
        if self.motion.done:
            self.motion = self.next_motion(t)
            vel = self.motion.velocity(t)
        else:
            self.count = self.count
        return vel


class Sin(RefInput):

    def __init__(self, param, t_init=0.0):
        super().__init__(param, t_init=t_init)

    @property
    def amplitude(self):
        return self.param['amplitude']

    @property
    def period(self):
        return self.param['period']

    def velocity(self,t):
        t_rel = self.t_rel(t)
        vx = 0.0
        vy = 0.0
        if t_rel >= 0.0:
            self.count = int(np.floor(t_rel/self.period))
            vx = self.amplitude*np.sin(2.0*np.pi*t_rel/self.period)
        else:
            self.count = -1
        return np.array([vx, vy])


class SinSeries(BaseSeries):

    def __init__(self, param, t_init=0.0):
        super().__init__(param, t_init=t_init)
        self.motion_model = Sin

    @property
    def motion_param(self): 
        motion_param = { 
                'amplitude' : self.amplitude(self.count),
                'period'    : self.period(self.count),
                't_settle'  : self.t_settle,
                'max_count' : self.cycles-1,
                }
        return motion_param

    def amplitude(self, num):
        return self.param['amplitude']

    def period(self, num):
        return self.param['period']


class SinPeriodSeries(SinSeries):

    def __init__(self, param, t_init=0.0):
        super().__init__(param, t_init=t_init)
        self.motion = DoneMotion({}) 
        self.is_first = True

    @property
    def period_list(self):
        return self.param['period_list']

    @property
    def repetitions(self):
        return len(self.period_list)

    def period(self, num):
        return self.period_list[num]


class Step(RefInput):

    def __init__(self, param, t_init=0.0):
        super().__init__(param, t_init=t_init)

    @property
    def amplitude(self):
        return self.param['amplitude']

    @property
    def period(self):
        return self.param['period']

    def velocity(self,t):
        t_rel = self.t_rel(t)
        vx = 0.0
        vy = 0.0
        if t_rel >= 0.0:
            s = float(t_rel%self.period)/self.period
            self.count = int(np.floor(t_rel/self.period))
            if s <= 0.5:
                sign = 1.0
            else:
                sign = -1.0
            vx = sign*self.amplitude
        else:
            self.count = -1 
        return np.array([vx,vy])


class StepSeries(BaseSeries):

    def __init__(self, param, t_init=0.0):
        super().__init__(param, t_init=t_init)
        self.motion_model = Step 

    @property
    def motion_param(self):
        motion_param = { 
                'amplitude' : self.amplitude(self.count),
                'period'    : self.period(self.count),
                't_settle'  : self.t_settle,
                'max_count' : self.cycles-1,
                }
        return motion_param

    def amplitude(self, num):
        return self.param['amplitude']

    def period(self, num):
        return self.param['period']


class StepZeroStep(RefInput):

    def __init__(self, param, t_init=0.0):
        super().__init__(param, t_init=t_init)

    @property
    def amplitude(self):
        return self.param['amplitude']

    @property
    def t_step(self):
        return self.param['t_step']

    @property
    def t_zero(self):
        return self.param['t_zero']

    @property
    def t_total(self):
        return 2*(self.t_step + self.t_zero)

    def velocity(self,t):
        t_rel = self.t_rel(t)
        vx = 0.0
        vy = 0.0
        if t_rel >= 0.0:
            t_mod = t_rel % self.t_total
            self.count = int(np.floor(t_rel/(0.5*self.t_total)))
            if t_mod < self.t_step:
                vx = self.amplitude
            elif t_mod < (self.t_step + self.t_zero):
                vx = 0.0
            elif t_mod < (2*self.t_step + self.t_zero):
                vx = -self.amplitude
            else:
                vx = 0.0
        else:
            self.count = -1
        return np.array([vx, vy])


class RandomStep(RefInput):

    def __init__(self, param, t_init=0.0):
        super().__init__(param, t_init=t_init)
        self.t_last = None
        self.duration = None
        self.cur_velocity = None

    @property
    def max_velocity(self):
        return self.param['max_velocity']

    @property
    def min_velocity(self):
        return self.param['min_velocity']

    @property
    def max_duration(self):
        return self.param['max_duration']

    @property
    def min_duration(self):
        return self.param['min_duration']

    def velocity(self,t):
        t_rel = self.t_rel(t)
        vx = 0.0
        vy = 0.0
        if t_rel >= 0.0:
            if (self.t_last is None) or (t_rel > (self.t_last + self.duration)):
                self.count += 1
                self.t_last = t_rel
                rand_val = np.random.rand()
                delta_duration = self.max_duration - self.min_duration
                self.duration = self.min_duration + rand_val*delta_duration 
                rand_val = np.random.rand()
                delta_velocity = self.max_velocity - self.min_velocity
                self.curr_velocity = self.min_velocity + rand_val*delta_velocity
            vx = self.curr_velocity
        else:
            self.count = -1
        return np.array([vx,vy])


class CyclicChirp(RefInput):

    def __init__(self, param, t_init=0.0):
        super().__init__(param, t_init=t_init)

    @property
    def amplitude(self):
        return self.param['amplitude']

    @property
    def min_freq(self):
        return self.param['min_freq']

    @property
    def max_freq(self):
        return self.param['max_freq']

    @property
    def n_cycles(self):
        return int(self.param['n_cycles'])

    @property
    def method(self):
        return self.param['method']

    @property
    def chirp_t1(self):
        if self.method == 'linear':
            val =  2.0*self.n_cycles/(self.max_freq + self.min_freq)
        elif self.method == 'logarithmic':
            val = self.n_cycles*np.log(self.max_freq/self.min_freq)
            val = val/(self.max_freq - self.min_freq)
        return val

    @property 
    def period(self):
        return 2*self.chirp_t1

    def velocity(self,t):
        t_rel = self.t_rel(t)
        vx = 0.0
        vy = 0.0
        if t_rel >= 0.0:
            self.count = int(np.floor(t_rel/self.period))
            if t_rel%self.period <= 0.5*self.period:
                s = t_rel%(0.5*self.period)
                f0 = self.min_freq
                t1 = self.chirp_t1
                f1 = self.max_freq
                vx = sig.chirp(s,f0,t1,f1,method=self.method,phi=-90)
            else:
                s = t_rel%self.period - 0.5*self.period
                f0 = self.max_freq
                t1 = self.chirp_t1
                f1 = self.min_freq
                vx = sig.chirp(s,f0,t1,f1,method=self.method,phi=-90)
            vx = self.amplitude*vx
        else:
            self.count = -1
        return np.array([vx,vy])





# -----------------------------------------------------------------------------
if __name__ == '__main__':

    import matplotlib.pyplot as plt

    param = {
            'amplitude'  : 400.0,
            'min_freq'   : 1/60.0, 
            'max_freq'   : 1/1.0, 
            'n_cycles'   : 10,  
            't_settle'   : 10.0,
            'method'     : 'logarithmic',
            }

    motion_model = CyclicChirp(param)
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
