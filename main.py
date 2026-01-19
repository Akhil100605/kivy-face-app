from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from camera4kivy import Preview
from kivy.uix.button import Button
from android.permissions import request_permissions, Permission


class CamApp(App):
    def build(self):
        request_permissions([Permission.CAMERA])

        layout = BoxLayout(orientation="vertical")

        self.preview = Preview(
            aspect_ratio="fit",
            camera_id="0"   # back camera
        )

        btn = Button(
            text="Switch Camera",
            size_hint_y=None,
            height=60
        )
        btn.bind(on_press=self.switch_camera)

        layout.add_widget(self.preview)
        layout.add_widget(btn)

        return layout

    def switch_camera(self, *args):
        self.preview.camera_id = "1" if self.preview.camera_id == "0" else "0"


if __name__ == "__main__":
    CamApp().run()
