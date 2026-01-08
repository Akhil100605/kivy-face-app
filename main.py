from kivy.core.window import Window
Window.rotation = 0

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.graphics import Scale, Translate


class CameraApp(App):

    def build(self):
        self.cam_index = 0   # 0 = back, 1 = front

        layout = BoxLayout(orientation='vertical')

        self.camera = Camera(index=self.cam_index, play=True, resolution=(640, 480))

        # 🔥 FIX MIRROR HERE
        with self.camera.canvas.before:
            self.scale = Scale(x=-1, y=1, z=1)
            self.translate = Translate()

        self.camera.bind(size=self.update_transform, pos=self.update_transform)

        layout.add_widget(self.camera)

        btn = Button(text="Switch Camera", size_hint_y=None, height=60)
        btn.bind(on_press=self.switch_camera)
        layout.add_widget(btn)

        return layout

    def update_transform(self, *args):
        self.translate.x = -self.camera.x * 2 - self.camera.width
        self.translate.y = 0

    def switch_camera(self, *args):
        self.cam_index = 1 if self.cam_index == 0 else 0
        self.camera.index = self.cam_index


if __name__ == "__main__":
    CameraApp().run()
