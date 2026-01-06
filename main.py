from kivy.app import App
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        return  Label(text="App started successfully")

if __name__ == "__main__":
    TestApp().run()
