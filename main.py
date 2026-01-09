import cv2
import numpy as np

from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class OpenCVCamera(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cam_index = 0
        self.capture = cv2.VideoCapture(self.cam_index)

        Clock.schedule_interval(self.update, 1.0 / 30)

    def switch_camera(self):
        self.cam_index = 1 if self.cam_index == 0 else 0
        self.capture.release()
        self.capture = cv2.VideoCapture(self.cam_index)

    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            return

        # ✅ FIX ORIENTATION
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # ✅ MIRROR FRONT CAMERA
        if self.cam_index == 1:
            frame = cv2.flip(frame, 1)

        # BGR -> RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to texture
        buf = frame.tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()

        self.texture = texture


class CameraApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")

        self.cam = OpenCVCamera()
        layout.add_widget(self.cam)

        btn = Button(text="Switch Camera", size_hint_y=None, height=60)
        btn.bind(on_press=lambda x: self.cam.switch_camera())
        layout.add_widget(btn)

        return layout


if __name__ == "__main__":
    CameraApp().run()

