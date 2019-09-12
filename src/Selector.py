import os
from pynput import keyboard
from pynput import mouse

import curses

class Item:

    dir_suffix = 'dir'

    NORMAL = "\033[01;00;00m"
    SELECTED = "\033[01;31;00m"
    HOVERED = "\033[01;32m" 
    strformat = NORMAL

    def __init__(self, name):
       
        self.fullname = name
        splitname = name.rsplit('.', 1) #splitting the string into pre and suffix
        self.name = splitname[0]
        try:
            self.suffix = splitname[1]
            self.isDir = False #cannot enter directory.d directories!
        except:
            self.suffix = self.dir_suffix
            self.isDir = True

        self.hovered = False
        self.selected = False
    
    def getSelectorItem(self) :
        return self.name

    def addSelectorItem(self, selectorwin):
        if self.hovered :
            selectorwin.addstr(self.name + '\n', curses.A_STANDOUT)
        else :
            selectorwin.addstr(self.name + '\n')

    def setHovered(self, hovered):
        self.hovered = hovered
        self.updateStrFormat()

    def setSelected(self, selected):
        self.selected = selected
        self.updateStrFormat()

    def updateStrFormat(self):
        if self.selected : 
            self.strformat = self.SELECTED
        elif self.hovered :
            self.strformat = self.HOVERED
        else :
            self.strformat = self.NORMAL

class Selector:


    def __init__(self, item_strings):
        
        self.items = []
        self.currentIndex = 0

        for item_string in item_strings:
            self.items.append(Item(item_string))

        self.listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release)
        
    def getDisplayString(self):
        out = '' 
        
        for item in self.items : 
            out += item.getSelectorItem() + "\n"
        
        return out

    def updateSelectorDisplay(self, selectorWin):
        for item in self.items :
            item.addSelectorItem(selectorWin)


    def up(self):
        self.dehover(self.currentIndex)
        self.currentIndex -= 1
        if self.currentIndex < 0 :
            self.currentIndex = len(self.items) - 1 
        self.hover(self.currentIndex)

    def down(self):
        self.dehover(self.currentIndex)
        self.currentIndex += 1
        if self.currentIndex == len(self.items) :
            self.currentIndex = 0
        self.hover(self.currentIndex)
        

    def selectItem(self):
        if self.items[self.currentIndex].selected :
            self.deselect(self.currentIndex)
        else :
            self.select(self.currentIndex)
        

    def hover(self, index):
        self.items[index].setHovered(True)

    def dehover(self, index):
        self.items[index].setHovered(False)

    def select(self, index):
        self.items[index].setSelected(True)

    def deselect(self, index):
        self.items[index].setSelected(False)
    
    def on_press(self, key):
        if key == keyboard.Key.up :
            self.up()
        elif key == keyboard.Key.down :
            self.down()
        elif key == keyboard.Key.space :
            self.selectItem()
        elif key == keyboard.Key.esc : 
            return False

    def on_release(self, key):
        return

    def listen(self):
        self.listener.join()

    def start(self) : 
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as self.listener:
            os.system('stty -echo') 
            self.listener.join() 
