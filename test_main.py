# @dnaspider

import time
import win32api
import win32com
import win32con

#global
strand=''
re='' #clone

#settings
show_outs=True
frequency=0.150
ctrl_scan_only_mode=False
speed=0 #0.555
database='c:/pdpy/database.txt'
#settings='c:/pdpy/settings.txt'
ctrl_key=win32con.VK_RCONTROL #toggle <
repeat_key=win32con.VK_SCROLL

def kb_clear_all(): #reset keys
    win32api.GetAsyncKeyState(repeat_key)
    win32api.GetAsyncKeyState(ctrl_key)
    win32api.GetAsyncKeyState(win32con.VK_ESCAPE)
    win32api.GetAsyncKeyState(ord('A'))
    win32api.GetAsyncKeyState(ord('B'))
    win32api.GetAsyncKeyState(ord('C'))

def scan(): # x:, x-, x:>, x->, <x:, <x-, <x:>, <x->, <x>, x>
    global strand, speed, database, re
    with open(database) as db:
        for cell in db:
            if cell[0:len(strand)+1]==strand + ':' or cell[0:len(strand)+1]==strand + '-' or cell[0:len(strand)+1]==strand + '>' :
                if show_outs: print('found:',strand)
                if cell[len(strand)]=='-': #auto backspace
                    for i in range(len(strand)):
                        if strand[i]=='<' or strand[i]=='.': continue #filter < .
                        win32api.keybd_event(win32con.VK_BACK, 0, 0, 0)
                        win32api.keybd_event(win32con.VK_BACK, 0, 2, 0)
                tail=cell[len(strand)+1:len(cell)]
                if tail[-1]=='\n': tail=cell[len(strand)+1:len(cell)-1] #filter \n if not last line
                if tail[0]=='>': tail=tail[1:] #filter >
                kb_event(tail)         
                re=tail
                strand=''           #reset
                kb_clear_all()      #
                #if speed>0: speed=0 #
                db.close()
                break

def key(k): #grow strand then scan
    global strand
    strand+=k
    if show_outs: print(strand)
    scan()

def kb_press(k, n):
    x=1
    for x in range(n):
        win32api.keybd_event(k, 0, 0, 0)
        win32api.keybd_event(k, 0, 2, 0)
    x+=1

def kb_event(k):
    global speed
    i=0
    while i < len(k):   
        win32api.GetAsyncKeyState(win32con.VK_ESCAPE) #clear
        if win32api.GetAsyncKeyState(win32con.VK_ESCAPE): #stop
            #if speed>0: speed=0
            break

        if k[i]=='<' and len(k)!=1:
            #cases ??
            if k[i+1]==',': 
                if k[i:i+3]=='<,>':
                    time.sleep(0.150)
                    k=k[k.find('>')+1:len(k)] #re i
                    continue
            #if k[i+1]=='a':
                #
            if k[i+1]=='b':
                if k[i:i+4]=='<bs>':
                    kb_press(win32con.VK_BACK,1)
                    k=k[k.find('>')+1:len(k)]
                    continue
                if k[i:i+4]=='<bs*':
                    n=int(k[k.find('*')+1:k.find('>')]) #get num
                    kb_press(win32con.VK_BACK,n)
                    k=k[k.find('>')+1:len(k)]
                    continue
            #if k[i+1]=='c':
                #
            if k[i+1]=='s': 
                if k[i:i+7]=='<sleep:':
                    n=int(k[k.find(':')+1:k.find('>')])
                    time.sleep(n)
                    k=k[k.find('>')+1:len(k)]
                    continue                    
                if k[i:i+7]=='<speed:':
                    n=int(k[k.find(':')+1:k.find('>')])
                    speed=n
                    k=k[k.find('>')+1:len(k)]
                    continue
                    
            #connect
            if k.find(':>') or k.find('->') and k.find('<',1) < (k.find(':>') or k.find('->')) and (k[1]!=':' or k[1]!='-'):
                con=k[0:k.find('>')+1] #<x:> or <x->
                global database
                with open(database) as db:
                    for cell in db:
                        if cell[0:len(con)]==con:
                            p=k[len(con):len(k)] #pre
                            o=cell[len(con):len(cell)]
                            if o[-1]=='\n': o=cell[len(con):len(cell)-1]
                            k=o+p
                            db.close()
                            break

        shift=False #init shift hold
        x=k[i] #init ord
        if ((ord(x) >= 33 and ord(x) <= 38) or (ord(x) >= 40 and ord(x) <= 43) or ord(x) == 58 or ord(x) == 60 or (ord(x) >= 62 and ord(x) <= 91) or ord(x) == 94 or ord(x) == 95 or (ord(x) >= 123 and ord(x) <= 126)): #if must hold shift
            shift = True 
        if shift: win32api.keybd_event(win32con.VK_LSHIFT, 0, 1, 0)
        win32api.keybd_event(win32api.VkKeyScan(x), 0, 0, 0) #kb press
        win32api.keybd_event(win32api.VkKeyScan(x), 0, 2, 0) #kb release
        if shift: 
            win32api.keybd_event(win32con.VK_LSHIFT, 0, 2, 0)
            win32api.keybd_event(win32con.VK_RSHIFT, 0, 2, 0)
        if speed>0: time.sleep(speed)
        k=k[1:len(k)] #++

def kb_release(k):
    win32api.keybd_event(k, 0, 2, 0)

def kb_clear(k): #clear individual key
    win32api.GetAsyncKeyState(k)

# def load_settings():
#     return
    
#input
# load_settings()
kb_clear_all()
while True:
    time.sleep(frequency)
    if win32api.GetAsyncKeyState(ord('\b')): #backspace
        strand=strand[:-1]
        if show_outs: print(strand)
    if win32api.GetAsyncKeyState(ctrl_key):
        if strand.startswith('<'):
            strand=''
            if show_outs: print(strand)
        else: 
            kb_clear_all()
            strand='<'
            if show_outs: print(strand)
    if win32api.GetAsyncKeyState(repeat_key): 
        if re > '': 
            kb_event(re)
            kb_clear_all()
            strand=''
    if ctrl_scan_only_mode and not strand.startswith('<') : continue    
    if win32api.GetAsyncKeyState(win32con.VK_ESCAPE): 
        kb_release(win32con.VK_ESCAPE)
        kb_clear(win32con.VK_ESCAPE)        
        key('.')
    if win32api.GetAsyncKeyState(ord('A')): key('a')
    if win32api.GetAsyncKeyState(ord('B')): key('b')
    if win32api.GetAsyncKeyState(ord('C')): key('c')