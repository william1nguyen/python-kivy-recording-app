from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from config import ENV

Builder.load_file("./views/components/rounded_button.kv")
Builder.load_file("./views/signup.kv")


class SignupWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_signup(self):
        username = self.ids.username.text
        email = self.ids.email.text
        password = self.ids.password.text
        password_confirm = self.ids.password_confirm.text

        print(username, email, password, password_confirm)
