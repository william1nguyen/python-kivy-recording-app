from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from controller import login, signup, main
from kivy.core.window import Window
from kivy.config import ConfigParser

config = ConfigParser()
config.read("config.ini")

WINDOW_WIDTH = int(config.get("settings", "WINDOW_WIDTH"))
WINDOW_HEIGHT = int(config.get("settings", "WINDOW_HEIGHT"))


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class App(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

    def on_pause(self):
        return super().on_pause()

    def build(self):
        window_manager = WindowManager()

        signup_window = signup.SignupWindow()
        window_manager.add_widget(signup_window)

        login_window = login.LoginWindow()
        window_manager.add_widget(login_window)

        # main_window = main.MainWindow()
        # window_manager.add_widget(main_window)

        return window_manager


if __name__ == "__main__":
    app = App()
    app.run()
