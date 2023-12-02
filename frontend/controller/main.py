import os
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty

Builder.load_file("./views/components/rounded_button.kv")
Builder.load_file("./views/main.kv")

dirname = os.path.dirname(__file__).replace("/controller", "")


class MainWindow(Screen):
    MICRO_ON_IMG_SRC = os.path.join(dirname, "views/assets/micro.jpeg")
    MICRO_OFF_IMG_SRC = os.path.join(dirname, "views/assets/micro.png")
    REWIND_BUTTON_IMG_SRC = os.path.join(dirname, "views/assets/rewind-button.png")
    FORWARD_BUTTON_IMG_SRC = os.path.join(dirname, "views/assets/forward-button.png")
    RECORD_ON_IMG_SRC = os.path.join(dirname, "views/assets/record_on.png")
    RECORD_OFF_IMG_SRC = os.path.join(dirname, "views/assets/record_off.png")

    is_recorded = False
    audio = ObjectProperty()
    time = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)

    def turn_on_signal(self):
        self.ids.record_signal.source = self.RECORD_ON_IMG_SRC

    def turn_off_signal(self):
        self.ids.record_signal.source = self.RECORD_OFF_IMG_SRC

    def turn_on_mic(self):
        self.ids.micro.source = self.MICRO_ON_IMG_SRC

    def turn_off_mic(self):
        self.ids.micro.source = self.MICRO_OFF_IMG_SRC

    def start_recording(self):
        self.audio.start()
        self.turn_on_signal()
        self.turn_on_mic()
        self.is_recorded = True

    def stop_recording(self):
        self.audio.stop()
        self.turn_off_signal()
        self.turn_off_mic()
        self.is_recorded = False

    def play_recording(self):
        state = self.audio.state
        if state == "playing":
            self.audio.stop()
        else:
            self.audio.play()
