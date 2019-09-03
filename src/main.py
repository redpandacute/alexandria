#!/sr/bin/env python3

import sys
import os
import curses
import curses.textpad

from Selector import Selector
from Selector import Item

import Command

try:
    from pynput import keyboard 
except ImportError:
    sys.exit('requires pynput, install it by doing: pip3 install Pynput')

inpt = '' 
active = True

CMD_TOKEN = 'x>'


def main():
    #print('hello')
    #command = input(':>')
    #x = Command.Command(command)
    
    global stdscr
    global inptwin
    global dirwin

    stscr = curses.initscr()
    inptwin = curses.newwin(1, curses.COLS, curses.LINES -1, 0)
    dirwin = curses.newwin(1000, curses.COLS, 0, 0)

    gui()


def gui():

    global inpt
    global active
    global stdscr
    global inptwin
    global dirwin
    global selector


    if active:

        selector = Selector([Item('num1'),Item('num2'),Item('num3'),Item('num4')])
        selector.updateSelectorDisplay(dirwin)
        #dirwin.addstr(selector.getDisplayString())
        dirwin.refresh()
        inptwin.addstr('x>')
        inptwin.refresh()
        
        start()
    
    


def on_press(key) :
    global inpt
    global selecto
    global dirwin
    global inptwin

    if(key == keyboard.Key.up) :
        selector.up()
        dirwin.clear()
        selector.updateSelectorDisplay(dirwin)
        #dirwin.addstr(selector.getDisplayString())
        dirwin.refresh()
        updateInptWin()
    elif key == keyboard.Key.down :
        selector.down()
        dirwin.clear()
        selector.updateSelectorDisplay(dirwin)
        #dirwin.addstr(selector.getDisplayString())
        dirwin.refresh()
        updateInptWin()
    elif key == keyboard.Key.space :
        inpt += ' '
        updateInptWin()
    elif key == keyboard.Key.backspace :
        inpt = inpt[:-1]
        updateInptWin()
    else :
        try :
            inpt += key.char
        except AttributeError:
            pass
        updateInptWin()

def updateInptWin():
    global inptwin

    inptwin.clear()
    inptwin.addstr(CMD_TOKEN + inpt)
    inptwin.refresh()


def on_release(key) :
    return


def listen():
    listener = keyboard.Listener(
        on_press = on_press,
        on_release = on_release
        )
    listener.join()


def start():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
#avoiding calls of the mainfunction on import
if __name__ == '__main__':
    main() 
