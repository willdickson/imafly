from __future__ import print_function
import time
import serial
import threading
import numpy as np


class TeensyPot(serial.Serial):

    Baudrate = 115200
    ResetSleepDt = 0.5
    MaxQueueSize = 1000
    Timeout = 10.0

    def __init__(self,param):
        serial_device_param = {
                'baudrate' : self.Baudrate, 
                'timeout'  : self.Timeout
                }
        super().__init__(param['port'],**serial_device_param)
        self.max_value = param['max_value']
        self.min_value = param['min_value']
        time.sleep(self.ResetSleepDt)
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.x = 0.0

    @property
    def vals(self):
        return np.array([self.x, 0.0])

    @property
    def x(self):
        with self.lock:
            x = self._x
        return x

    @x.setter
    def x(self,new_x):
        with self.lock:
            self._x = new_x

    def start(self):
        self.stop_event.clear()
        self.write('b\n'.encode())
        worker = threading.Thread(target=self.receive_data)
        worker.daemon = True
        worker.start()

    def stop(self):
        self.write('e\n'.encode())
        self.stop_event.set()

    def receive_data(self):
        while not self.stop_event.is_set():
            try:
                line = self.readline()
            except serial.serialutil.SerialException as err:
                print(f'serial exception {err}')
                continue
            line = line.strip()
            try:
                self.x = 2.0*(float(line) - self.min_value)/self.max_value - 1.0
            except ValueError as err:
                print(f'ValueError: {err}')
                continue
            except TypeError as err:
                print(f'TypeError: {err}')
                continue
        self.stop_event.clear()



# ------------------------------------------------------------------------------------

if __name__ == '__main__':

    param = {
            'port'      : '/dev/ttyACM0',
            'min_value' : 0.0,
            'max_value' : 3.3, 
            }

    dev = TeensyPot(param)
    dev.start()

    t0 = time.time()
    while time.time() - t0 < 4.0:
        print(dev.vals)

    dev.stop()

