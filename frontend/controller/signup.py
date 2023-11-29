from config import *
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from .popup import Popup
import requests

Builder.load_file("./views/components/rounded_button.kv")
Builder.load_file("./views/signup.kv")

PASSWORD_MIN_LENGTH = 8


class User:
    def __init__(self, _username, _email, _password, _password_confirm) -> None:
        self.username = _username
        self.email = _email
        self.password = _password
        self.password_confirm = _password_confirm


class SignupWindow(Screen):
    is_signed_up = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def is_valid_text(self, text):
        if not text:
            return False
        return True

    def is_valid(self, user):
        for prop in vars(user).values():
            if not self.is_valid_text(prop):
                return False
        return True

    def on_signup(self):
        username = self.ids.username.text
        email = self.ids.email.text
        password = self.ids.password.text
        password_confirm = self.ids.password_confirm.text

        user = User(username, email, password, password_confirm)

        if not self.is_valid(user):
            popup = Popup("Error", "Missing Fields!")
            popup.open()
        elif user.password != user.password_confirm:
            popup = Popup("Error", "Password didn't match!")
            popup.open()
        elif len(user.password) < PASSWORD_MIN_LENGTH:
            popup = Popup("Error", "Password didn't reach minimum length")
            popup.open()
        else:
            url = BASE_URL + "/api/signup"
            data = {
                "username": username,
                "email": email,
                "password": password,
                "password_confirm": password_confirm,
            }
            response = requests.request("POST", url=url, data=data)
            response_data = response.json()

            if response.status_code == 201:
                popup = Popup("Alert", response_data.get("message"))
                popup.open()
                self.is_signed_up = True
            else:
                popup = Popup("Error", response_data.get("errors"))
                popup.open()
