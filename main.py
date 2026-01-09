from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

from android.permissions import request_permissions, Permission

request_permissions([
    Permission.CAMERA,
    Permission.READ_EXTERNAL_STORAGE,
    Permission.WRITE_EXTERNAL_STORAGE
])


class CamApp(App):

    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.msg = Label(text="Waiting for permission...")
        self.layout.add_widget(self.msg)

        self.camera = Camera(play=False, resolution=(320, 240))
        self.layout.add_widget(self.camera)

        btn = Button(text="Capture Photo", size_hint_y=None, height=60)
        btn.bind(on_press=self.capture)
        self.layout.add_widget(btn)

        # 🔥 start camera AFTER UI loads
        Clock.schedule_once(self.start_camera, 1)

        return self.layout

    def start_camera(self, dt):
        self.camera.play = True
        self.msg.text = "Camera started"

    def capture(self, *args):
        self.camera.export_to_png("/sdcard/test_face.png")
        self.msg.text = "Saved to /sdcard/test_face.png"


if __name__ == "__main__":
    CamApp().run()
 
