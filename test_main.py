# @dnaspider

import time
import win32api
import win32com
import win32con
import pynput
from pynput.keyboard import Key, Controller


keyboard=Controller()


strand=''

#settings...
frequency=0.150
ctrl_scan_only_mode=True
#...settings

def clear_kb():
    win32api.GetAsyncKeyState(ord('A'))
    win32api.GetAsyncKeyState(ord('B'))
    win32api.GetAsyncKeyState(ord('C'))

def scan():
    global strand
    if strand == 'abc':
        print('found')
        strand=''
        keyboard.type('123')

def key(k):
    global strand
    strand+=k
    print(strand)
    scan()
    #e.cancel()

clear_kb()
while True:
    time.sleep(frequency)
    if win32api.GetAsyncKeyState(ord('\b')):#backspace
        strand=strand[:-1]
    if win32api.GetAsyncKeyState(win32con.VK_RCONTROL):
        if strand.startswith('<'): strand=''
        else: 
            clear_kb()
            strand='<'
            print(strand)
    if ctrl_scan_only_mode and not strand.startswith('<') : continue
    if win32api.GetAsyncKeyState(win32con.VK_ESCAPE): key('.')
    if win32api.GetAsyncKeyState(ord('A')): key('a')
    if win32api.GetAsyncKeyState(ord('B')): key('b')
    if win32api.GetAsyncKeyState(ord('C')): key('c')

