from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from .popup import Popup

Builder.load_file("./views/components/rounded_button.kv")
Builder.load_file("./views/login.kv")


class LoginWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_login(self):
        username = self.ids.username.text
        password = self.ids.password.text

        if not username or not password:
            popup = Popup("Error", "Missing Fields")
            popup.open()

        