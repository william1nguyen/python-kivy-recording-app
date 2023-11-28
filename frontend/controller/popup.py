from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty


WINDOW_POPUP_WIDTH = 500
WINDOW_POPUP_HEIGHT = 800


class Popup(Popup):
    def __init__(self, _title, _message, **kwargs):
        super().__init__(**kwargs)

        self.title = _title
        self.content = Label(text=_message)
        self.size_hint = (None, None)
        self.size = (WINDOW_POPUP_HEIGHT, WINDOW_POPUP_WIDTH)


class OptionPopup(Popup):
    message = ObjectProperty("")
    callback = ObjectProperty(None, allownone=True)

    def __init__(self, _title, _message, **kwargs):
        self.register_for_motion_event("on_answer")
        super().__init__(**kwargs)
        self.title = _title
        self.message = _message
        self.size_hint = (None, None)
        self.size = (WINDOW_POPUP_HEIGHT, WINDOW_POPUP_WIDTH)

    def on_answer(self, answer):
        if self.callback:
            self.callback(answer)
        self.dismiss()
