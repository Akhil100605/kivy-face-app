from kivy.core.window import Window
Window.rotation = 0
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.clock import Clock

from android.permissions import request_permissions, Permission


class CamApp(App):
    def build(self):
        request_permissions([Permission.CAMERA])

        layout = BoxLayout(orientation="vertical")

        self.cam = Camera(play=True, resolution=(640, 480))
        self.cam.allow_stretch = True
        self.cam.keep_ratio = True

        layout.add_widget(self.cam)
        layout.add_widget(Label(text="Camera ON 📸"))

Clock.schedule_once(self.fix_camera, 1)
        return layout

    def fix_camera(self, dt):
        # rotate camera texture to portrait
        if self.cam.texture:
            self.cam.rotation = 90
self.cam.texture.flip_vertical()


if __name__ == "__main__":
    CamApp().run()
