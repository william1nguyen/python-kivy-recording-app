import os
import shutil

import kivy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plyer
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView

'''

'''
class YesNoPopup(Popup): 
    message = ObjectProperty('')
    callback = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super(YesNoPopup, self).__init__(**kwargs)
        self.title = 'Alert'
        self.size_hint = (None, None)
        self.size = (800, 500)

    def on_answer(self, answer):
        if self.callback:
            self.callback(answer)
        self.dismiss()

class AlertPopup(Popup):
    def __init__(self, **kwargs):
        super(AlertPopup, self).__init__(**kwargs)
        self.title = 'Alert'
        self.content = Label(text='')
        self.size_hint = (None, None)
        self.size = (800, 500)


class DataManagementSystem:

    '''
        @param self                ...
        
        @var idSentence:            ID of a sentence (number)
        @var numberOfSenteces:      Number of Sentences in dataset

        @list sentenceList:         Store all the sentences in data input 

        @dict database:             Point that which sentences is matched with current ID
    '''
    def __init__(self) -> None:
        self.idSentence = 0
        self.numberOfSentences = 0
        self.sentenceList = []
        self.database = {}

        self.build()

    '''
        @param self                ...
        
        Initlize varaibles in class
    '''
    def build(self):
        with open('./Info/data.txt', encoding="utf8") as reader:
            for sentence in reader:
                sentence = self.transform(sentence.replace('\n', ''))
                self.sentenceList.append(sentence)
                self.database[sentence] = self.idSentence
                self.idSentence = self.idSentence + 1

        self.numberOfSentences = len(self.sentenceList)

        self.idSentence = self.numberOfSentences - 1  # return the end sentence

    '''
        @param self                ...
        @param str : input string need to transform
        @param limitWordPerLine :   ...
        
        @var currentWord:           Current word are being created
        @var wordCounterPerLine:    Count number of word in current line
        
        @return createSentence:     String after transformation 
         
        Transform sentence to multiple line by limiting word per line.
    '''
    def transform(self, str, limitWordPerLine=30) -> str:
        currentWord = ''
        wordCounterPerLine = 0
        createSentence = ''
        for character in str + ' ':
            if character == ' ':  # a word has been commited
                wordCounterPerLine = wordCounterPerLine + 1
                if wordCounterPerLine == limitWordPerLine:
                    createSentence = createSentence + currentWord + '\n'
                    wordCounterPerLine = 0
                else:
                    createSentence = createSentence + currentWord + ' '
                currentWord = ''
            else:
                currentWord = currentWord + character
        return createSentence


# create data systme
dataSystem = DataManagementSystem()


class AudioManagementSystem:
    def __init__(self) -> None:
        self.hasRecord = False              # commit that exist a record file
        self.savePath = './audio/'

    '''
        @param self
        @param audio:                   default in this app is plyer.audio
        @param idPerson                 current speaker ID
        
        Save record file to des foldre
    '''

    def create_container(self):
        dirPath = self.savePath + 'speaker_' + '{0:03}'.format(idPerson)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

    def saveAudio(self, audio, idPerson):
        srcFile = str(audio.file_path).replace('file://', '')
        desFile = self.savePath + 'speaker_' + \
            '{0:03}'.format(idPerson) + '/audio' + \
            str(dataSystem.idSentence + 1) + '.wav'

        dirPath = self.savePath + 'speaker_' + '{0:03}'.format(idPerson)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        shutil.copy(srcFile, desFile)

    def addAudio(self):
        self.hasRecord = True


audioSystem = AudioManagementSystem()


class LoginWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.saveFailed = False

    '''
        @param self                
        
        @var id:                                        Current speaker ID
        @var name, age, gender, phone, region:          Speaker information about age, birth year, gender, phone number, hometown
        @var saveFailed:                                Check if all information has been filled
        
        @table dataframe:                               Speaker information database
        
        @return:                                        None
    '''
    def saveInformation(self):
        id = None
        with open('./Info/speakerId.txt', 'r') as reader:
            for Id in reader:
                id = int(Id)
        name = self.ids['name'].text
        age = self.ids['age'].text
        gender = self.ids['gender'].text
        phone = self.ids['phone'].text
        region = self.ids['region'].text

        if name == '' or age == '' or gender == '' or phone == '' or region == '': # check if all information has been filled
            self.saveFailed = True
            return

        dataframe = pd.read_csv('./Info/speaker.csv', sep=',')
        data = list(zip([id], [name], [age], [gender], [phone], [region]))

        columns = dataframe.columns
        newSpeaker = pd.DataFrame(data=data, columns=columns)

        dataframe = pd.concat((dataframe, newSpeaker), axis=0)
        dataframe.to_csv('./Info/speaker.csv', index=False)

        self.saveFailed = False

        self.ids['name'].text = ''
        self.ids['age'].text = ''
        self.ids['gender'].text = ''
        self.ids['phone'].text = ''
        self.ids['region'].text = ''


class OptionWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AppWindow(Screen):
    '''
        @var global idPerson:               Current speaker ID (int)
        @var canCreateSpeaker:              Fill the condition of adding speaker or not (boolean)  
        
        @dict  checked:                     mark all recorded sentence as True and vice versa
        
        ! audio = plyer.audio
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global idPerson
        idPerson = 0
        
        with open('./Info/speakerId.txt', 'r') as reader:
            for id in reader:
                idPerson = int(id)          # get current ID on file

        self.canReRecord = False
        self.checked = {}
        self.canCreateSpeaker = True

    audio = ObjectProperty()
    time = NumericProperty(0)

    '''
        @param self
        
        Confirm yes/no base on speaker want to re recording current sentence or not.
    '''
    def confirmReRecoringPopup(self):
        yesnoPopup = YesNoPopup(
            message='Do you want to re-recording this?', callback=self.answerReRecordingPopup)
        yesnoPopup.open()

    '''
        @param self
        @param answer:              answer of yes/no question for re-recording
    '''
    def answerReRecordingPopup(self, answer):
        if answer == True:
            self.audio.start()
            self.ids.recordImage.source = './asserts/micro.jpeg'        # turn on micro
            self.ids.recordSignal.source = './asserts/record_on.png'    # turn the record signal on
            self.turnOnWave()  # display wave

    '''
        @param self
        
        confirm yes/no base on speaker want to skip current sentence or not.
    '''
    def confirmSkipPopup(self):
        yesnoPopup = YesNoPopup(
            message='Do you want to skip this sentence?', callback=self.answerSkipPopup
        )
        yesnoPopup.open()
    
    '''
        @param self
        @param answer:              answer of yes/no question for skipping
    '''
    def answerSkipPopup(self, answer):
        if answer == True:
            self.nextRecording(flag=1)
            
    
    def conditionAddSpeaker(self):
        return dataSystem.idSentence == dataSystem.numberOfSentences - 1  # if current sentence is not the last sentence

    '''
        @param self
        
        @var global idPerson:                       ID of current speaker
    
        Temporary add speaker but not submit it to database
    '''
    def addSpeaker(self):
        self.canCreateSpeaker = self.conditionAddSpeaker()
        if not self.canCreateSpeaker:
            return

        global idPerson
        idPerson = idPerson + 1

        audioSystem.create_container()

        for id in range(dataSystem.numberOfSentences):
            self.checked[id] = False        # mark all sentence didn't record
        
        dataSystem.idSentence = 0         # text display now return first sentence in data store

        # increase speaker in database
        with open('./Info/speakerId.txt', 'w') as writer:
            writer.write(str(idPerson))
            
        self.updateCurrentSentenceDisplay()
        self.updateTextLabels()

    
    '''
        @param self
        
        @var state:                         Current app state 
        
        Start recording function
    '''
    def startRecording(self):
        if idPerson == 0:   # check if there exist at least one speaker
            return

        state = self.audio.state
        if state == 'ready':
            # check if this sentence has been recorded
            if self.checked[dataSystem.idSentence] == True:
                self.confirmReRecoringPopup()
            else:
                self.audio.start()
                self.ids.recordSignal.source = './asserts/record_on.png'  # turn the record signal on
                self.turnOnWave()  # display wave

        if state == 'recording':
            self.audio.stop()
            self.turnOffWave()  # turn off wave
           
            self.ids.recordSignal.source = './asserts/record_off.png'  # turn off the record signal

            self.checked[dataSystem.idSentence] = True

            
            audioSystem.saveAudio(self.audio, idPerson) # save and move file from temp directory to des directory
            audioSystem.addAudio()  # new audio has been commited

        self.updateTextLabels()


    '''
        @param self
        
        @var state:                         Current app state 
        
        Play the latest record audio that speaker've just created
    '''
    def playRecording(self):
        if idPerson == 0:
            return

        state = self.audio.state
        if state == 'playing':
            self.audio.stop()
        else:
            self.audio.play()

        self.updateTextLabels()

    '''
        @param self
        
        Switch to previus sentence
    '''
    def prevRecording(self):
        if idPerson == 0:
            return

        if dataSystem.idSentence == 0: # current sentence is not the first sentence
            return

        # alert ("Do you want to replace older file")

        state = self.audio.state
        if state == 'ready':
            state = 'prev'
            dataSystem.idSentence = dataSystem.idSentence - 1

        self.updateTextLabels()
        self.updateCurrentSentenceDisplay()

    '''
        @param self
        @param flag (default=0):                        check if this sentence has been recorded
        
        Switch to next sentence
    '''
    def nextRecording(self, flag=0):
        if idPerson == 0:
            return

        if flag == 0:
            if self.checked[dataSystem.idSentence] == False:  # did'nt record this sentece
                self.confirmSkipPopup()
                return

        if dataSystem.idSentence == dataSystem.numberOfSentences - 1:    #if recorded the last sentence
            alertPopup = AlertPopup()
            alertPopup.content = Label(text='Congratulation! You are finish! Please Add Speaker')
            alertPopup.open()
            return

        state = self.audio.state
        if state == 'ready':
            state = 'next'
            dataSystem.idSentence = dataSystem.idSentence + 1

        self.updateTextLabels()
        self.updateCurrentSentenceDisplay()

    '''
        @param self
        
        Update label on each button after some changes
    '''
    def updateTextLabels(self):
        recordButton = self.ids['recordButton']
        playButton = self.ids['playButton']
        stateLabel = self.ids['stateLabel']
        nextButton = self.ids['nextButton']
        prevButton = self.ids['prevButton']
        newSpeakerButton = self.ids['addSpeaker']
        backButton = self.ids['backButton']
        
        lstButton = [recordButton, playButton, nextButton, prevButton, newSpeakerButton, backButton]

        state = self.audio.state
        stateLabel.text = 'AudioPlayer State: ' + state

        playButton.disabled = not audioSystem.hasRecord         # disabled play button if there don't exsit any audio record yet.

        if state == 'ready':
            for button in lstButton:
                button.disabled = False                         # all button are enable when state is 'ready'

        if state == 'recording':
            for button in lstButton: 
                if button != recordButton:
                    button.disabled = True                      # all button are disable except 'recordButton' when state is 'recording'

        if state == 'playing':
            playButton.text = 'Stop'
            for button in lstButton: 
                if button != playButton:
                    button.disabled = True                      # all button are disable except 'playButton' when state is 'playing'
        else:
            playButton.text = 'Press to play'
            recordButton.disabled = False

        if state == 'prev':
            state = 'ready'

        if state == 'next':
            state = 'ready'

        if dataSystem.idSentence == dataSystem.numberOfSentences - 1:     # current sentence is the last sentence or not
            self.ids['speakerLabel'].text = 'Please Add Speaker!'
        else:
            self.ids['speakerLabel'].text = 'Speaker ' + \
                '{0:03} : '.format(idPerson)  # update speaker label

        if self.checked[dataSystem.idSentence] == False:                # current sentence is recorded or not
            self.ids['recordImage'].source = './asserts/micro.jpeg'
        else:
            self.ids['recordImage'].source = './asserts/micro.png'
            
    '''
        @param self
        
        Update display sentence content
    '''        
    def updateCurrentSentenceDisplay(self):
        currentSentence = dataSystem.sentenceList[dataSystem.idSentence]
        self.ids['textLabel'].text = currentSentence

    def turnOnWave(self):
        pass

    def turnOffWave(self):
        pass

class FolderScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.ids['filechooser'].path = os.path.join(os.getcwd(), 'Audio/' + 'speaker_' + \
            '{0:03}'.format(idPerson))  # change datapath for filechooser

    '''
        @param self
        @param path:                           path to the selected directory (a list)       

        @var filename:                          name of the selected audio remove all character before '/'
        @var id:                               ID of current audio that is selected
        @var file:                              path to the selected directory (a string) 
    '''         
    def selected(self,path):
        try: 
            filename = str(path[-1]).rsplit('/', 1)[-1]
            id = int(''.join(i for i in filename if i.isdigit()))
            
            # display text to check with audio file
            self.ids.textPopup.text = dataSystem.transform(str=dataSystem.sentenceList[id - 1].replace('\n', ' '), limitWordPerLine=18)
            
            file = str(path[-1])
            os.system("afplay " + file) # play path audio 
            
            self.ids.filechooser.selection = []  # remove all selection to rechoose folder
        except:
            pass
    
class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AudioApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.maximize()       # make window fit to speaker laptop screen

    def build(self):  
        windowManager = WindowManager()

        loginWindow = LoginWindow()
        windowManager.add_widget(loginWindow)

        optionWindow = OptionWindow()
        windowManager.add_widget(optionWindow)

        appWindow = AppWindow()
        appWindow.addSpeaker()
        windowManager.add_widget(appWindow)

        folderScreen = FolderScreen()
        windowManager.add_widget(folderScreen)

        return windowManager

    def on_pause(self):
        return True


if __name__ == "__main__":
    AudioApp().run()
