from picamera2 import Picamera2

class Singleton(type):
    camera = None

    def __call__(cls, *args, **kwargs):
        if camera == None:
            camera = super().__call__(*args, **kwargs)
        return camera

class Camera(metaclass=Singleton):
    def __init__(self, size, buffer=4, mode='still'):
        self._buffer = buffer
        self._cam = Picamera2()
        if mode == 'still':
            self._config = picam2.create_still_configuration()
        elif mode == 'video':
            self._config = picam2.create_video_configuration()
    
    def get_info(self):
        return {
            'mode': self.mode
        }
    
    @property
    def cam(self):
        return self._cam

