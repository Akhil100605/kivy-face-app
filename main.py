from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from android.permissions import request_permissions, Permission

from camera4kivy import Preview


class CamApp(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.preview = Preview(
            play=True,
            resolution=(1280, 720)
        )

        layout.add_widget(self.preview)

        btn = Button(text="Switch Camera", size_hint_y=None, height=60)
        btn.bind(on_press=self.switch_camera)
        layout.add_widget(btn)

        return layout

    def on_start(self):
        request_permissions([Permission.CAMERA])

    def switch_camera(self, *args):
        # 0 = back, 1 = front
        self.preview.camera_id = 1 if self.preview.camera_id == 0 else 0


if __name__ == "__main__":
    CamApp().run()

