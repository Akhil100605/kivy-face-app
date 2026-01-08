from kivy.core.window import Window
Window.rotation = 0

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Scale
from android.permissions import request_permissions, Permission


class RotatedCamera(Camera):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate(angle=270, origin=self.center)
            self.scale = Scale(x=1, y=-1, z=1, origin=self.center)
        with self.canvas.after:
            PopMatrix()
        self.bind(pos=self.update_transform, size=self.update_transform)

    def update_transform(self, *args):
        self.rot.origin = self.center
        self.scale.origin = self.center

class CamApp(App):
    def build(self):
        request_permissions([Permission.CAMERA])

        layout = BoxLayout(orientation="vertical")

        cam = RotatedCamera(play=True, resolution=(640, 480))
        cam.allow_stretch = True
        cam.keep_ratio = True

        layout.add_widget(cam)
        layout.add_widget(Label(text="Camera ON"))

        return layout


if __name__ == "__main__":
    CamApp().run()
