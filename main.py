from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from android.permissions import request_permissions, Permission

import cv2
import numpy as np


class CamApp(App):
    def build(self):
        self.img = Image()
        self.cap = None
        return self.img

    def on_start(self):
        request_permissions([Permission.CAMERA])
        Clock.schedule_once(self.start_camera, 1)

    def start_camera(self, dt):
        self.cap = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        if not self.cap:
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        # rotate if needed (try ROTATE_90_CLOCKWISE if wrong)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # mirror fix (for front camera look)
        frame = cv2.flip(frame, 1)

        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture


if __name__ == "__main__":
    CamApp().run()

