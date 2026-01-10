from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from android.permissions import request_permissions, Permission
from camera4kivy import Preview

import cv2
import numpy as np


class CamApp(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.preview = Preview(
            play=True,
            resolution=(640, 480),
            on_frame=self.on_frame
        )

        layout.add_widget(self.preview)

        btn = Button(text="Switch Camera", size_hint_y=None, height=60)
        btn.bind(on_press=self.switch_camera)
        layout.add_widget(btn)

        return layout

    def on_start(self):
        request_permissions([Permission.CAMERA])

    def switch_camera(self, *args):
        self.preview.camera_id = 1 if self.preview.camera_id == 0 else 0

    def on_frame(self, frame):
        # frame is numpy array (BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # just test processing (no face yet)
        edges = cv2.Canny(gray, 50, 150)

        # show processed frame
        self.preview.texture_from_numpy(edges)


if __name__ == "__main__":
    CamApp().run()
