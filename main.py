from kivy.app import App
from kivy.uix.bonlayout import BoxLayout

class TestApp(App):
    def build(self):
        return  BoxLayout()

if __name__ == "__main__":
    FaceApp().run()
