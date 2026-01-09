from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button


class CameraApp(App):
    def build(self):
        self.cam_index = 0  # 0 = back, 1 = front

        layout = BoxLayout(orientation='vertical')

        self.camera = Camera(
            index=self.cam_index,
            play=True,
            resolution=(1280, 720),
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=False   # FULL SCREEN
        )

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
