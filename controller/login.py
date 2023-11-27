from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from config import ENV

Builder.load_file("./views/components/rounded_button.kv")
Builder.load_file("./views/login.kv")


class LoginWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_login(self):
        username = self.ids.username.text
        password = self.ids.password.text
