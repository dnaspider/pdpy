# @dnaspider

import time
import win32api
import win32com
import win32con

#global
strand=''

#settings
show_outs=True
frequency=0.150
ctrl_scan_only_mode=False
speed=0 #0.555
database='c:/dna/db.txt'

def kb_clear_all(): #reset_keys
    win32api.GetAsyncKeyState(win32con.VK_RCONTROL)
    win32api.GetAsyncKeyState(win32con.VK_ESCAPE)
    win32api.GetAsyncKeyState(ord('A'))
    win32api.GetAsyncKeyState(ord('B'))
    win32api.GetAsyncKeyState(ord('C'))

def scan(): # x:, x-, x:>, x->, <x:, <x-, <x:>, <x->, <x>, x>
    global strand, speed, database
    with open(database) as db:
        for cell in db:
            if cell[0:len(strand)+1]==strand + ':' or cell[0:len(strand)+1]==strand + '-' or cell[0:len(strand)+1]==strand + '>' :
                if show_outs: print('found:',strand)
                if cell[len(strand)]=='-': #bs
                    for i in range(len(strand)):
                        if strand[i]=='<' or strand[i]=='.': continue #filter_<
                        win32api.keybd_event(win32con.VK_BACK, 0, 0, 0)
                        win32api.keybd_event(win32con.VK_BACK, 0, 2, 0)
                tail=cell[len(strand)+1:len(cell)]
                if tail[-1]=='\n': tail=cell[len(strand)+1:len(cell)-1] #filter_\n_if_not_last_line
                if tail[0]=='>': tail=tail[1:] #filter_>
                kb_event(tail)         
                strand=''           #reset
                kb_clear_all()      #
                if speed>0: speed=0 #C

def key(k): #grow_strand_then_scan
    global strand
    strand+=k
    scan()
    if show_outs: print(strand)

def kb_event(k):
    global speed
    for i in k: 
        win32api.GetAsyncKeyState(win32con.VK_ESCAPE)#clear
        if win32api.GetAsyncKeyState(win32con.VK_ESCAPE):#stop
            #if speed>0: speed=0
            break
        shift=False #init_shift_hold
        if ((ord(i) >= 33 and ord(i) <= 38) or (ord(i) >= 40 and ord(i) <= 43) or ord(i) == 58 or (ord(i) >= 62 and ord(i) <= 91) or ord(i) == 94 or ord(i) == 95 or (ord(i) >= 123 and ord(i) <= 126)): #if must hold shift
            shift = True 
        if shift: win32api.keybd_event(win32con.VK_LSHIFT, 0, 1, 0)
        win32api.keybd_event(win32api.VkKeyScan(i), 0, 0, 0)#kb_press
        win32api.keybd_event(win32api.VkKeyScan(i), 0, 2, 0)#kb_release
        if shift: 
            win32api.keybd_event(win32con.VK_LSHIFT, 0, 2, 0)
            win32api.keybd_event(win32con.VK_RSHIFT, 0, 2, 0)
        if speed>0: time.sleep(speed)
        

def kb_release(k):
    win32api.keybd_event(k, 0, 2, 0)

def kb_clear(k): #clear_individual_key
    win32api.GetAsyncKeyState(k)

    
#input                
kb_clear_all() 
while True:
    time.sleep(frequency)
    if win32api.GetAsyncKeyState(ord('\b')):#backspace
        strand=strand[:-1]
        if show_outs: print(strand)
    if win32api.GetAsyncKeyState(win32con.VK_RCONTROL):
        if strand.startswith('<'):
            strand=''
            if show_outs: print(strand)
        else: 
            kb_clear_all()
            strand='<'
            if show_outs: print(strand)
    if ctrl_scan_only_mode and not strand.startswith('<') : continue    
    if win32api.GetAsyncKeyState(win32con.VK_ESCAPE): 
        kb_release(win32con.VK_ESCAPE)
        kb_clear(win32con.VK_ESCAPE)        
        key('.')
    if win32api.GetAsyncKeyState(ord('A')): key('a')
    if win32api.GetAsyncKeyState(ord('B')): key('b')
    if win32api.GetAsyncKeyState(ord('C')): key('c')