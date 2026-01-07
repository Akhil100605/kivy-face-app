from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label

from android.permissions import request_permissions, Permission


class CamApp(App):
    def build(self):
        request_permissions([Permission.CAMERA])

        layout = BoxLayout(orientation="vertical")

        self.cam = Camera(play=True, resolution=(640, 480))
        layout.add_widget(self.cam)

        layout.add_widget(Label(text="Camera ON 📸"))

        return layout


if __name__ == "__main__":
    CamApp().run()
