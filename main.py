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

        Clock.schedule_once(self.fix_rotation, 1)
        return layout

    def fix_rotation(self, dt):
        # rotate camera texture to portrait
        if self.cam.texture:
            self.cam.texture.flip_vertical()
            self.cam.rotation = 90


if __name__ == "__main__":
    CamApp().run()
