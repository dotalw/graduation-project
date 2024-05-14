from libcamera import controls
from picamera2 import Picamera2


class Camera:
    def __init__(self):
        self.camera = Picamera2()
        self.camera.configure(
            self.camera.create_preview_configuration(
                main={"format": 'XRGB8888', "size": (1536, 864)}
            )
        )
        self.camera.start()
        self.camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

    def capture_frame(self):
        return self.camera.capture_array()
