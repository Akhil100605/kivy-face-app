from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rotate, Scale

from android.permissions import request_permissions, Permission

request_permissions([
    Permission.CAMERA,
    Permission.READ_EXTERNAL_STORAGE,
    Permission.WRITE_EXTERNAL_STORAGE
])

# lock portrait
Window.rotation = 0


class CamApp(App):

    def build(self):
        self.cam_index = 0  # 0=back, 1=front

        layout = BoxLayout(orientation='vertical')

        self.msg = Label(text="Starting camera...")
        layout.add_widget(self.msg)

        self.camera = Camera(
            play=False,
            resolution=(640, 480),
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=True,
            index=self.cam_index
        )
        layout.add_widget(self.camera)

        with self.camera.canvas.before:
            self.rot = Rotate(angle=180, origin=self.camera.center)
            self.scale = Scale(x=1, y=1, z=1)

        self.camera.bind(center=self.update_transform)

        btn_layout = BoxLayout(size_hint_y=None, height=60)

        switch_btn = Button(text="Switch Camera")
        switch_btn.bind(on_press=self.switch_camera)

        cap_btn = Button(text="Capture")
        cap_btn.bind(on_press=self.capture)

        btn_layout.add_widget(switch_btn)
        btn_layout.add_widget(cap_btn)

        layout.add_widget(btn_layout)

        Clock.schedule_once(self.start_camera, 1)
        return layout

    def update_transform(self, *args):
        self.rot.origin = self.camera.center
        self.scale.origin = self.camera.center

    def start_camera(self, dt):
        self.camera.play = True
        self.msg.text = "Camera running"

    def switch_camera(self, *args):
        self.cam_index = 1 if self.cam_index == 0 else 0
        self.camera.play = False
        self.camera.index = self.cam_index

        # mirror only front camera
        if self.cam_index == 1:
            self.scale.x = -1
        else:
            self.scale.x = 1

        Clock.schedule_once(lambda dt: setattr(self.camera, "play", True), 0.5)
        self.msg.text = "Switched camera"

    def capture(self, *args):
        path = "/sdcard/test_face.png"
        self.camera.export_to_png(path)
        self.msg.text = f"Saved: {path}"


if __name__ == "__main__":
    CamApp().run()
