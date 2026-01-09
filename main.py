from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from camera4kivy import Preview


class CamApp(App):

    def build(self):
        layout = BoxLayout(orientation="vertical")

        self.preview = Preview(play=True)

        btn = Button(text="Switch Camera", size_hint_y=None, height=60)
        btn.bind(on_press=self.switch_camera)

        layout.add_widget(self.preview)
        layout.add_widget(btn)
        return layout

    def switch_camera(self, *args):
        if self.preview.camera_id == "0":
            self.preview.camera_id = "1"
        else:
            self.preview.camera_id = "0"


if __name__ == "__main__":
    CamApp().run()
