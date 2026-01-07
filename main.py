from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)

        label = Label(text="✅ App started successfully", font_size=24)
        btn = Button(text="Click Me", size_hint=(1, 0.3))

        btn.bind(on_press=self.on_button_click)

        layout.add_widget(label)
        layout.add_widget(btn)
        return layout

    def on_button_click(self, instance):
        print("Button clicked!")


if __name__ == "__main__":
    TestApp().run()
