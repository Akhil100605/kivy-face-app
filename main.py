from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2
import numpy as np


class CamApp(App):
    def build(self):
        self.img = Image()
        self.cap = cv2.VideoCapture(0)

        Clock.schedule_interval(self.update, 1 / 30)
        return self.img

    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # mirror fix

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
        self.cap.release()


if __name__ == "__main__":
    CamApp().run()
