from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from camera4kivy import Preview

from android.permissions import request_permissions, Permission


class CamApp(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.preview = Preview()
        layout.add_widget(self.preview)

        btn = Button(text="Switch Camera", size_hint_y=None, height=60)
        btn.bind(on_press=self.switch_camera)
        layout.add_widget(btn)

        return layout

    def on_start(self):
        request_permissions([Permission.CAMERA], self.start_camera)

    def start_camera(self, permissions, results):
        if Permission.CAMERA in permissions:
            self.preview.connect_camera(enable_analyze=False)

    def switch_camera(self, *args):
        self.preview.toggle_camera()


if __name__ == "__main__":
    CamApp().run()

