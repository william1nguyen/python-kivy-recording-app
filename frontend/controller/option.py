from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file("./views/components/rounded_button.kv")
Builder.load_file("./views/option.kv")


class OptionWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)