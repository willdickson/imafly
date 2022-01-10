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
        self.time_step = param['time_step']
        self.h5_logger = h5_logger.H5Logger(param['data_file'], param_attr=param)

    def run(self):

        t_init = time.time()
        t_last = 0.0 

        while True:

            t_curr = time.time() - t_init
            dt = t_curr - t_last
            if dt <= self.time_step:
                continue

            self.plant.update(t_curr, dt)
            self.stimulus.update(t_curr, dt)
            image = self.stimulus.display_image(self.plant.pos)
            error = self.stimulus.vel - self.plant.vel

            cv2.imshow('image', image)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
            t_last = t_curr
            data = {
                    't'            : t_curr,
                    'v_stimulus'   : self.stimulus.vel,
                    'v_plant'      : self.plant.vel,
                    'v_error'      : error, 
                    'cnt_stimulus' : self.stimulus.motion.count,
                    }
            self.h5_logger.add(data)

            print(f't: {t_curr:0.3f}', end='') 
            print(f', dt: {dt:0.3f}', end='')
            print(f', vx: {self.plant.vel[0]:0.3f}', end='')  
            print(f', vy: {self.plant.vel[1]:0.3f}', end='')
            print(f', e: {error[0]:0.3f}', end='')
            print(f', cnt: {self.stimulus.motion.count}')

        self.plant.stop()




