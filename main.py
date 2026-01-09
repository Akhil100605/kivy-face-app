from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Rotate, Scale, PushMatrix, PopMatrix
from android.permissions import request_permissions, Permission


class CameraApp(App):
    def build(self):
        request_permissions([Permission.CAMERA])

        Window.rotation = 0  # keep app portrait

        self.cam_index = 0
        self.layout = BoxLayout(orientation='vertical')

        self.add_camera()

        btn = Button(text="Switch Camera", size_hint_y=None, height=60)
        btn.bind(on_press=self.switch_camera)
        self.layout.add_widget(btn)

        return self.layout

    def add_camera(self):
        self.camera = Camera(index=self.cam_index, play=True)

        with self.camera.canvas.before:
            PushMatrix()
            self.rot = Rotate(angle=90, origin=self.camera.center)
            self.scale = Scale(x=-1 if self.cam_index == 1 else 1, y=1, z=1)

        with self.camera.canvas.after:
            PopMatrix()

        self.camera.bind(pos=self.update_transform, size=self.update_transform)

        self.layout.add_widget(self.camera, index=1)

    def update_transform(self, *args):
        self.rot.origin = self.camera.center

    def switch_camera(self, *args):
        self.layout.remove_widget(self.camera)
        self.camera.play = False

        self.cam_index = 1 if self.cam_index == 0 else 0
        self.add_camera()


if __name__ == "__main__":
    CameraApp().run()


