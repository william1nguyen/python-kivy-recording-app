from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from .popup import Popup
import requests
from config import *

Builder.load_file("./views/components/rounded_button.kv")
Builder.load_file("./views/login.kv")

PASSWORD_MIN_LENGTH = 8


class LoginWindow(Screen):
    is_signed_in = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def reset_input(self):
        self.ids.email.text = ""
        self.ids.password.text = ""

    def on_login(self):
        email = self.ids.email.text
        password = self.ids.password.text

        if not email or not password:
            popup = Popup("Error", "Missing Fields")
            popup.open()
        elif len(password) < PASSWORD_MIN_LENGTH:
            popup = Popup("Error", "Password didn't reach minimum length")
            popup.open()

        else:
            url = BASE_URL + "/api/login"
            data = {
                "email": email,
                "password": password,
            }
            response = requests.post(url=url, data=data, verify=False)
            response_data = response.json()

            if response.status_code == 200:
                self.is_signed_in = True
            else:
                popup = Popup("Error", response_data.get("errors"))
                popup.open()

        self.reset_input()
