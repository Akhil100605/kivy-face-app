import cv2
import numpy as np   # ✅ IMPORTANT

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from android.permissions import request_permissions, Permission


class OpenCVCamera(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cam_index = 0
        self.capture = None
        self.start_camera()

        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def start_camera(self):
        if self.capture:
            self.capture.release()

        self.capture = cv2.VideoCapture(self.cam_index)

    def switch_camera(self):
        self.cam_index = 1 if self.cam_index == 0 else 0
        self.start_camera()

    def update(self, dt):
        if not self.capture or not self.capture.isOpened():
            return

        ret, frame = self.capture.read()
        if not ret:
            return

        # ✅ rotate to portrait
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        # ✅ mirror only front camera
        if self.cam_index == 1:
            frame = cv2.flip(frame, 1)

        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]),
            colorfmt='bgr'
        )
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture


class CameraApp(App):
    def build(self):

        request_permissions([
            Permission.CAMERA,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])

        layout = BoxLayout(orientation='vertical')

        self.cam = OpenCVCamera()
        layout.add_widget(self.cam)

        btn = Button(text="Switch Camera", size_hint_y=None, height=60)
        btn.bind(on_press=lambda x: self.cam.switch_camera())
        layout.add_widget(btn)

        return layout

    def on_stop(self):
        if self.cam.capture:
            self.cam.capture.release()


if __name__ == "__main__":
    CameraApp().run()
