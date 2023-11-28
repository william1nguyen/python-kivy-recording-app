from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file("./views/main.kv")


class MainWindow(Screen):
    is_recorded = False

    def __init__(self, **kw):
        super().__init__(**kw)
