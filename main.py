from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.clock import Clock


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.label = Label(text="Camera not started", size_hint=(1, 0.1))
        self.add_widget(self.label)

        self.cam = Camera(play=False, resolution=(640, 480), size_hint=(1, 0.8))
        self.add_widget(self.cam)

        self.btn = Button(text="Start Camera", size_hint=(1, 0.1))
        self.btn.bind(on_press=self.start_camera)
        self.add_widget(self.btn)

    def start_camera(self, instance):
        self.label.text = "Camera ON 📸"
        self.cam.play = True


class TestApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    TestApp().run()
