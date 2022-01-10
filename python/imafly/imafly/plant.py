import numpy as np
from . import joystick
from . import teensy_pot

class Plant:

    def __init__(self, param):
        self.input = self.get_input_handler(param['input'])
        self.model = self.get_plant_model(param['model'])

    def stop(self):
        self.input.stop()

    def update(self, t, dt):
        self.model.update(t, dt, self.input.vals)

    @property
    def vel(self):
        return self.model.vel

    @property
    def pos(self):
        return self.model.pos

    @staticmethod
    def get_input_handler(input_param):
        if input_param['type'] == 'joystick':
            input_handler = joystick.JoyStick(input_param)
        elif input_param['type'] == 'teensy':
            input_handler = teensy_pot.TeensyPot(input_param)
            input_handler.start()
        else:
            raise RuntimeError(f'unknown input type {param["type"]}')
        return input_handler

    @staticmethod
    def get_plant_model(model_param):
        if model_param['type'] == 'velocity':
            model = ProportionalVelocityPlant(model_param)
        elif model_param['type'] == 'integral':
            model = IntegralVelocityPlant(model_param)
        else:
            raise RuntimeError(f'unknown model type {param["type"]}')
        return model


class ProportionalVelocityPlant:
    """ 
    Implements a plant where the velocity is proportional to the input signal.

    """

    def __init__(self, param):
        self.gain = np.array([param['xgain'], param['ygain']])
        self.vel = np.array([0.0, 0.0])
        self.pos = np.array([0.0, 0.0])

    def update(self, t, dt, input_val):
        self.vel = self.gain*input_val
        self.pos += dt * self.vel


class IntegralVelocityPlant:

    """
    Implements a plant where the velocity is an integral of the input signal.

    """

    def __init__(self, param):
        self.gain = np.array([param['xgain'], param['ygain']])
        self.damp = np.array([param['xdamp'], param['ydamp']])
        self.vel = np.array([0.0, 0.0])
        self.pos = np.array([0.0, 0.0])

    def update(self, t, dt, input_val):
        self.vel += ( self.gain*input_val - self.damp*self.vel ) * dt
        self.pos += dt * self.vel





