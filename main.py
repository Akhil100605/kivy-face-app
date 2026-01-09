from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from android.permissions import request_permissions, Permission

request_permissions([
    Permission.CAMERA,
    Permission.READ_EXTERNAL_STORAGE,
    Permission.WRITE_EXTERNAL_STORAGE
])
class CameraApp(App):
    def build(self):
        request_permissions([Permission.CAMERA])

        self.cam_index = 0

        layout = BoxLayout(orientation='vertical')

        self.camera = Camera(index=self.cam_index, play=True)

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

