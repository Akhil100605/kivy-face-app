from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2
import numpy as np

from android.permissions import request_permissions, Permission


class CamApp(App):
    def build(self):
        self.img = Image()
        self.cap = None

        request_permissions([Permission.CAMERA], self.on_permission)
        return self.img

    def on_permission(self, permissions, results):
        if all(results):
            self.cap = cv2.VideoCapture(0)
            Clock.schedule_interval(self.update, 1 / 30)

    def update(self, dt):
        if self.cap is None:
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)

        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]),
            colorfmt='rgb'
        )
        texture.blit_buffer(
            frame.tobytes(),
            colorfmt='rgb',
            bufferfmt='ubyte'
        )
        self.img.texture = texture

    def on_stop(self):
        if self.cap:
            self.cap.release()


if __name__ == "__main__":
    CamApp().run()


