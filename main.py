from kivy.core.window import Window
Window.rotation = 0
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button


class CameraApp(App):

    def build(self):
        self.cam_index = 0

        layout = BoxLayout(orientation='vertical')

        self.camera = Camera(index=0, play=True, resolution=(640, 480))
        self.camera.allow_stretch = True
        self.camera.keep_ratio = True

        layout.add_widget(self.camera)

        btn = Button(text="Switch Camera", size_hint_y=None, height=60)
        btn.bind(on_press=self.switch_camera)
        layout.add_widget(btn)

        return layout

    def switch_camera(self, *args):
        self.cam_index = 1 if self.cam_index == 0 else 0
        self.camera.index = self.cam_index


if __name__ == "__main__":
    CameraApp().run()
