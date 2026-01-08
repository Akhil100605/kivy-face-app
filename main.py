from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.clock import Clock


class CameraApp(App):

    def build(self):
        self.cam_index = 0  # 0 = back, 1 = front

        layout = BoxLayout(orientation='vertical')

        self.camera = Camera(index=self.cam_index, play=True, resolution=(640, 480))
        self.camera.allow_stretch = True
        self.camera.keep_ratio = True

        layout.add_widget(self.camera)

        btn = Button(text="Switch Camera", size_hint_y=None, height=60)
        btn.bind(on_press=self.switch_camera)
        layout.add_widget(btn)

        # wait for texture, then fix mirror if needed
        Clock.schedule_once(self.fix_texture, 1)

        return layout

    def fix_texture(self, dt):
        if self.camera.texture:
            # flip only if front camera
            if self.cam_index == 1:
                self.camera.texture.flip_horizontal()

    def switch_camera(self, *args):
        self.cam_index = 1 if self.cam_index == 0 else 0
        self.camera.index = self.cam_index

        # wait again for new camera texture
        Clock.schedule_once(self.fix_texture, 1)


if __name__ == "__main__":
    CameraApp().run()
