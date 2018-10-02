# @dnaspider

import time
from kivy.app import App
from kivy.uix.button import Label
from kivy.clock import Clock
import win32api
import win32com
import win32con
import pynput
from pynput.keyboard import Key, Controller
from kivy.config import Config
Config.set('kivy','exit_on_escape',0)
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout 


class Interface(GridLayout):
    def __init__(self, **kwargs):
        super(Interface,self).__init__(**kwargs)
        self.cols = 2
        
        global strand
        strand = Label(text = '')
        self.add_widget(strand)
        
        self.textbox = TextInput(multiline=True)
        self.add_widget(self.textbox)

class StaticApp(App):
    
    #title=''
    
    def build(self):        
        keyboard=Controller()
        
        #settings...
        frequency=0.150
        ctrl_scan_only_mode=False
        #...settings

        def scan():
            if strand.text == 'abc':
                print('found')
                strand.text=''
                keyboard.type('123')
        
        def key(k):
            strand.text+=k
            #print(strand)
            scan()
            #e.cancel()
        
        def echo(dt):#delta-time
            if win32api.GetAsyncKeyState(ord('\b')):#backspace
                strand.text=strand.text[:-1]
            if win32api.GetAsyncKeyState(win32con.VK_RCONTROL):
                if strand.text.startswith('<'): strand.text=''
                else: strand.text='<'
            if ctrl_scan_only_mode and not strand.text.startswith('<') : return
            if win32api.GetAsyncKeyState(win32con.VK_ESCAPE): key('.')
            if win32api.GetAsyncKeyState(ord('A')): key('a')
            if win32api.GetAsyncKeyState(ord('B')): key('b')
            if win32api.GetAsyncKeyState(ord('C')): key('c')
            #pass

        e = Clock.schedule_interval(echo, frequency)
        e()
        
        return Interface() 
        

if __name__ == '__main__': StaticApp().run()