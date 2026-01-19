from kivy app import App
from kivy.uix.label import Label
class TestApp(App):
    def build(self):
        return Label(text="APP OPENED SUCCESSFULLY",font_size=10)
if _name_=='_main_':
    TestApp().run()
