from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from datetime import datetime, timedelta
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from time import strftime
import re

pauses = []

class MainWindow(Screen):
    my_textinput = ObjectProperty(None)
    my_label = ObjectProperty(None)
    def btn(self):
        self.my_label.text += "\n" + self.my_textinput.text

class Kalender(Screen):
    pass

class Study(Screen):
    running = False  

    def start(self):       
        cd_time = self.ids.text_input.text 
        check = re.findall("[a-zA-Z]", cd_time)
        if cd_time == '' or len(cd_time) != 8 or check:
            self.ids.show.text = 'Please enter the time like this "00:00:05"'     
        elif cd_time == '00:00:00':
            Clock.unschedule(self.begin)
        elif self.ids.button.text == 'Reset':
            self.reset()
            
        else:
            self.ids.button.text = 'Reset'
            h = cd_time[0:2]
            m = cd_time[3:5]
            s = cd_time[6:8]
            h = int(h)
            m = int(m)
            s = int(s)
        
            self.delta = datetime.now() + timedelta(hours=h, minutes=m, seconds = s)
            if not self.running:
                    self.running = True
                    Clock.schedule_interval(self.begin, 0.05)
                      
    def reset(self): 
        
        self.ids.button.text = 'Start' 
        self.ids.show.text = 'Enter the time to countdown in this format "HH:MM:SS"\n For example, 00:00:30'
        self.ids.text_input.text = '00:00:00'
            
        if self.running:  
            self.running = False
            Clock.unschedule(self.begin)
            
    def pause(self):
        if self.running:  
            self.running = False
            Clock.unschedule(self.begin)
            self.ids.pause_button.text = 'Continue'
            pauses.append(datetime.now())
        elif self.ids.pause_button.text == 'Continue':
            self.running = True
            self.delta += (datetime.now()-pauses[-1])
            Clock.schedule_interval(self.begin, 0.05)
            self.ids.pause_button.text = 'Pause'
                

    def begin(self, cd_start):
        delta = self.delta - datetime.now()
        delta = str(delta)
        self.ids.show.text = delta[0:7]
        
        if delta[0:7]  == "0:00:00":
           
            '0' + delta[0:7]
            self.sound = SoundLoader.load('clock test\Breaking Bad Main Title Theme (Extended).mp3')
            self.sound.play()
            self.reset()   

    def toggle(self):
        if self.running:
            self.reset()
        else:
            self.start()  
    
    def update_padding(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width)/2

        max_lenght = 8
        if len(self.ids.text_input.text) > max_lenght:
            self.ids.text_input.text = self.ids.text_input.text[:-1]


class Challenges(Screen):
    pass

class Setting(Screen):
    pass


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("blob.kv")

class BlobMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    BlobMainApp().run()