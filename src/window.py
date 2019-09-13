import curses
import os
from Selector import Selector
from Selector import Item #Selectorfile should be renamed

class InputWindow():
    

    PROMPT = '~ '
    inputstr = ''

    def __init__(self, maxY, maxX):
        self.maxY = maxY
        self.maxX = maxX
        self.window = curses.newwin(1, self.maxX - 2, self.maxY - 2, 1)
        self.refresh()
        #self.window.addstr(self.PROMPT + self.inputstr)
        #self.window.border('|', '|', '-','-', '>', '<', '>','<')
    
    def redraw(self, new_maxY, new_maxX):
        global window
        global maxY
        global maxX

        self.maxY = new_maxY
        self.maxX = new_maxX


        self.window.resize(1, self.maxX - 2)    
        self.window.mvwin(self.maxY - 2, 1)

        #testing purposes
        #self.window.border('|', '|', '-','-', '>', '<', '>','<')
        self.window.erase()
        self.window.addstr(self.PROMPT + self.inputstr)
        self.window.refresh()

    def refresh(self):
        self.redraw(self.maxY, self.maxX)

    def addinput(self, inpt):
        global inputstr
        self.inputstr += inpt

    def backspace(self):
        global inputstr

        self.inputstr = self.inputstr[:-1]

    def flush(self):
        global inputstr

        self.inputstr = ''

#======================== reaction ============================

    def react(self, key):
    
        #ENTER == 10, BACKSPACE == 127, ESC == 27, up == 279165, down == 279166, right == 279167, left == 279168

        if key == 10: #ENTER
            #execute command in parser
            self.flush()
        elif key == 127: #BACKSPACE
            self.backspace()
        elif key > 256:
            pass
        else:
            #for getting key constants
            #self.addinput(str(key))
            try:
                self.addinput(chr(key))
            except:
                pass

        self.refresh()

class SelectorWindow():

    EMPTY_STRING = "[empty]"

    def __init__(self, dirPath, nlines = None, ncols = None, posY = None,  posX = None):
        
        self.dirPath = dirPath
        self.focused = False
        
        self.readPath(self.dirPath)

        self.ncols = ncols
        self.nlines = nlines
        self.posY = posY
        self.posX = posX
        self.currentIndex = 0

        

        if self.ncols is not None: #it is assumed that there isnt a method that constructs from null values
            self.minScrollPos = 0
            self.maxScrollPos = self.nlines - 2
            self.window = curses.newwin(self.nlines, self.ncols, self.posY, self.posX)
        else :
            self.window = None
        #self.window = screen.subwin(nlines, self.ncols, self.posY, self.posX)
        
        if self.items:
            self.items[self.currentIndex].setHovered(True)
            self.empty = False
        else:
            self.empty = True
        
    def redraw(self, new_nlines, new_ncols, new_posY, new_posX):
        global window
        global ncols
        global nlines
        global posY
        global posX
        global minScrollPos
        global maxScrollPos
        
        self.nlines = new_nlines
        self.ncols = new_ncols
        self.posY = new_posY
        self.posX = new_posX

        #provisorisch
        self.minScrollPos = 0
        self.maxScrollPos = self.nlines - 2
        
        #in case the window has not yet been initalized
        if self.window is None:
            self.window = curses.newwin(self.nlines, self.ncols, self.posY, self.posX)

        #updating directory
        self.updateDirectory()

        self.window.erase()

        

        #always resize before calling the move function
        self.window.resize(self.nlines, self.ncols) 
        self.window.mvwin(new_posY, new_posX)


        if self.items:
           self.addVisibleSelectorItems()
        elif self.nlines > 2 and self.ncols > 10:
           self.window.addstr(1,2, self.EMPTY_STRING)
        else:
           pass

        
        self.window.border('|', '|', '-','-', '#', '#', '#','#')
        self.window.refresh()

    #adds the currently visible SelectorItems to the display
    def addVisibleSelectorItems(self):

        i = 0
        for item in self.items:
            
            if len(item.name) + len(item.suffix) + 6 > self.ncols :
                #shortening the name (8 = 2 for spacing at edge, 2 for [], 3 for ... and 1 for ' ' 
                displaystr = '[' + item.suffix.upper() + '] ' + item.name[:self.ncols - len(item.name) - len(item.suffix) - 8] + '...'
            else :
                displaystr = '[' + item.suffix.upper() + '] ' + item.name
            
            displaystr += '\n'
            
            if i >= self.minScrollPos and i <= self.maxScrollPos :
                if item.hovered :
                    self.window.addstr(1 + i, 1, displaystr, curses.A_STANDOUT)
                    self.window.clrtoeol()
                else :
                    self.window.addstr(1 + i, 1, displaystr)
                    self.window.clrtoeol()
            
            i += 1
        

    def refresh(self):
        self.redraw(self.nlines, self.ncols, self.posY, self.posX)

    def readPath(self, path):
        self.items = []
        for item in os.listdir(path):
            self.items.append(Item(item))

    def updateDirectory(self):
        new_items = []
        for ositem in os.listdir(self.dirPath):
            for item in self.items:
                if item.fullname == ositem:
                    new_items.append(item)
                    added = True
                    break
            if not added:
                new_items.append(Item(ositem))
        self.items = new_items


        
#================================= Handling input and navigation ==================================

    def currentItem(self):
        return self.items[self.currentIndex]
    
    #selection and hovering
    def hover(self, index):
        self.items[index].setHovered(True)
        #TODO: add full name in topbar

    def dehover(self, index):
        self.items[index].setHovered(False)

    def select(self, index):
        if self.items[index].selected :
            self.items[index].setSelected(False)
        else :
            self.items[index].setSelected(True)


    #navigation
    def up(self):
        self.dehover(self.currentIndex)
        self.currentIndex -= 1
        if self.currentIndex  < 0 :
            self.currentIndex = len(self.items) - 1
            #TODO: adjust scrolling if necessary
        self.hover(self.currentIndex)
        self.refresh()

    def down(self):
        self.dehover(self.currentIndex)
        self.currentIndex += 1
        if self.currentIndex == len(self.items) :
            self.currentIndex = 0
        self.hover(self.currentIndex)
        self.refresh()
    
class DisplayWindow():

    def __init__(self, path, nlines = None, ncols = None, posY = None, posX = None):
        self.path = path
        self.nlines = nlines
        self.ncols = ncols
        self.posY = posY
        self.posX = posX
        
        if nlines:
            self.window = curses.newwin(self.nlines, self.ncols, self.posY, self.posX)
            self.refresh()
        else :
            self.window = None
       
    def redraw(self, new_path, new_nlines, new_ncols, new_posY, new_posX):
        self.nlines = new_nlines
        self.ncols = new_ncols
        self.posY = new_posY
        self.posX = new_posX

        self.path = new_path

        if self.window is None:
            self.window = curses.newwin(self.nlines, self.ncols, self.posY, self.posX)

        self.window.erase()

        self.window.resize(self.nlines, self.ncols)
        self.window.mvwin(self.posY, self.posX)

        #TODO ADD DRAWING FUNCTION FOR IMAGES
        self.window.addstr(1,1, self.path)

        self.window.border('|', '|', '-','-', '#', '#', '#','#')
        self.window.refresh()

    def refresh(self):
        self.redraw(self.path, self.nlines, self.ncols, self.posY, self.posX)

    def erase(self):
        self.window.erase()
        self.window.refresh()

    def setPath(self, path):
        self.path = path
        self.refresh()


