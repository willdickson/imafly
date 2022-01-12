import cv2
import time
import numpy as np
import h5_logger

from . import stimulus
from . import plant


class TrialRunner:

    def __init__(self,param):
        self.stimulus = stimulus.Stimulus(param['stimulus'])
        self.plant = plant.Plant(param['plant'])
        self.h5_logger = h5_logger.H5Logger(param['data_file'], param_attr=param)
        self.time_step = param['time_step']

    def run(self):

        t_init = time.time()
        t_last = 0.0 

        while not self.stimulus.done:

            # Check if it is time for next update
            t_curr = time.time() - t_init
            dt = t_curr - t_last
            if dt <= self.time_step:
                continue

            # Update plant model and stimulus
            self.plant.update(t_curr, dt)
            self.stimulus.update(t_curr, dt)

            # Display current stimulus image
            image = self.stimulus.display_image(self.plant.pos)
            cv2.imshow('image', image)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
            t_last = t_curr
            error = self.stimulus.vel - self.plant.vel

            # Log data to file
            data = {
                    't'              : t_curr,
                    'v_stimulus'     : self.stimulus.vel,
                    'v_plant'        : self.plant.vel,
                    'v_error'        : error, 
                    'stimulus_count' : self.stimulus.motion.count,
                    'is_trial'       : self.stimulus.motion.is_trial(t_curr),
                    'stimulus_event' : self.stimulus.motion.event,
                    }
            try:
                data['cycle_count'] = self.stimulus.motion.motion.count
            except AttributeError:
                pass
            try:
                data['cycle_event'] = self.stimulus.motion.motion.event
            except AttributeError:
                pass
            self.h5_logger.add(data)

            # Print run time info
            print(f't: {t_curr:0.3f}', end='') 
            print(f', dt: {dt:0.3f}', end='')
            print(f', sx: {self.stimulus.vel[0]:0.3f}', end='')  
            print(f', sy: {self.stimulus.vel[1]:0.3f}', end='')
            print(f', vx: {self.plant.vel[0]:0.3f}', end='')  
            print(f', vy: {self.plant.vel[1]:0.3f}', end='')
            print(f', e: {error[0]:0.3f}', end='')
            print(f', cnt: {self.stimulus.motion.count}')

        self.plant.stop()


