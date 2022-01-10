import cv2
import numpy as np

from . import ref_input

class Stimulus:

    def __init__(self, param):
        self.param = param
        self.image = create_image(param['image'])
        self.motion = self.get_motion_model(param['motion'])
        self.vel = np.array([0.0, 0.0])
        self.pos = np.array([0.0, 0.0])

    def update(self, t, dt):
        self.vel = self.motion.velocity(t)
        self.pos += dt*self.vel

    def display_image(self, input_pos):
        rel_pos = self.pos - input_pos
        image = np.roll(self.image, int(rel_pos[1]), axis=0)
        image = np.roll(image, int(rel_pos[0]), axis=1)
        if self.param['image']['type'] == 'ball':
            width = self.param['image']['width']
            height = self.param['image']['height']
            radius = int(1.5*self.param['image']['radius'])
            pos = (width//2, height//2)
            image = cv2.circle(image, pos, radius, (0,0,255), 5)
        return image

    @staticmethod
    def get_motion_model(motion_param):
        if motion_param['type'] == 'none':
            model = ref_input.NoMotion(motion_param)
        elif motion_param['type'] == 'sin':
            model = ref_input.Sin(motion_param)
        elif motion_param['type'] == 'step':
            model = ref_input.Step(motion_param)
        elif motion_param['type'] == 'step_zero_step':
            model = ref_input.StepZeroStep(motion_param)
        elif motion_param['type'] == 'random_step':
            model = ref_input.RandomStep(motion_param)
        elif motion_param['type'] == 'cyclic_chirp':
            model = ref_input.CyclicChirp(motion_param)
        else:
            raise RuntimeError(f'unknown motion type {motion_param["type"]}')
        return model


def create_image(param):
    image = None
    if param['type'] == 'vstripe':
        # Extract image parameters
        width  = param['width']
        height = param['height']
        number = param['number']
        color0 = param['color0']
        color1 = param['color1']
        # Create empty image
        image = np.zeros((height, width, 3), dtype=np.uint8)
        bndry = np.linspace(0, width, 2*number+1, dtype=np.int)
        bndry_pairs = zip(bndry[:-1], bndry[1:])
        for i, pair in enumerate(bndry_pairs):
            n,m = pair
            if i%2 == 0:
                image[:,n:m] = color0
            else:
                image[:,n:m] = color1
    elif param['type'] == 'ball':
        width  = param['width']
        height = param['height']
        color = param['color']
        radius = param['radius']
        image = np.zeros((height, width, 3), dtype=np.uint8)
        pos = ( width // 2, height // 2 )
        image = cv2.circle(image, pos, radius, color, -1)
    else:
        raise RuntimeError(f'unknown image type {param["type"]}')
    return image
