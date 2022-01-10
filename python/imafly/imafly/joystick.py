import inputs
import threading
import numpy as np

class JoyStick:

    def __init__(self,param):
        self.xcode = param['xcode']
        self.ycode = param['ycode']
        self.ximax = param['ximax']
        self.yimax = param['yimax']
        self.lock = threading.Lock()
        self.x = 0.0
        self.y = 0.0
        self.joystick_thread = threading.Thread(target=self.event_handler, daemon=True) 
        self.joystick_thread.start()

    def stop(self):
        """ Dummy method for compatibility is teensy_pot"""
        pass

    @property
    def vals(self):
        with self.lock:
            vals = np.array([self.x_val, self.y_val])
        return vals 

    @property
    def x(self):
        with self.lock:
            x = self.x_val
        return x

    @x.setter
    def x(self,value):
        with self.lock:
            self.x_val = value

    @property
    def y(self):
        with self.lock:
            y = self.y_val
        return y

    @y.setter
    def y(self,value):
        with self.lock:
            self.y_val = value

    def event_handler(self):
        while True:
            event_list = inputs.get_gamepad()
            for event in event_list:
                if event.code == self.xcode:
                    self.x = self.x_state_to_value(event.state)
                elif event.code == self.ycode:
                    self.y = self.y_state_to_value(event.state)

    def x_state_to_value(self,event_state):
        return 2.0 * float(event_state) / self.ximax - 1.0 

    def y_state_to_value(self,event_state):
        return 2.0 * float(event_state) / self.yimax - 1.0 
