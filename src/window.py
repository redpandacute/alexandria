import curses
from Selector import Selector
from Selector import Item

class InputWindow():
    

    PROMPT = ':-:'
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

    def addinput(self, key):
        global inputstr

        self.inputstr += key

    def backspace(self):
        global inputstr

        self.inputstr[:-1]
        self.refresh()

    def flush():
        global inputstr

        inputstr = ''
        self.refresh()

class SelectorWindow():

    EMPTY_STRING = "[empty]"

    def __init__(self, selectorItems, nlines = None, ncols = None, posY = None,  posX = None):
        
        self.focused = False
        self.selector = Selector(selectorItems)
        
        self.ncols = ncols
        self.nlines = nlines
        self.posY = posY
        self.posX = posX
        if self.ncols is not None: #it is assumed that there isnt a method that constructs from null values
            self.minScrollPos = 0
            self.maxScrollPos = self.nlines - 2
            self.window = curses.newwin(self.nlines, self.ncols, self.posY, self.posX)
        else :
            self.window = None
        #self.window = screen.subwin(nlines, self.ncols, self.posY, self.posX)


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

        self.window.erase()
        
        #always resize before calling the move function
        self.window.resize(self.nlines, self.ncols) 
        self.window.mvwin(new_posY, new_posX)


        if self.selector is not None:
           self.addVisibleSelectorItems()
        elif self.nlines > 2 and self.ncols > 10:
           self.window.addstr(1,2, self.EMPTY_STRING)
        else:
           pass

        #for testing
        self.window.border('|', '|', '-','-', '-', '-', '-','-')
        #self.window.border(' ','|',' ',' ',' ',' ',' ',' ')
        
        self.window.refresh()
    
    def addSelector(self, new_selector):
        global selector

        if isinstance(new_selector, Selector):
            if len(new_selector.items) > 0:
                self.selector = new_selector
                return 1
            self.selector = None
            return 0
        else:
            self.selector = None
            return 0
        self.refresh()

    #adds the currently visible SelectorItems to the display
    def addVisibleSelectorItems(self):
        i = 0
        for item in self.selector.items:
            
            if len(item.name) + len(item.suffix) + 6 > self.ncols :
                #shortening the name (8 = 2 for spacing at edge, 2 for [], 3 for ... and 1 for ' ' 
                displaystr = '[' + item.suffix + '] ' + item.name[:self.ncols - len(item.name) - len(item.suffix) - 8] + '...'
            else :
                displaystr = '[' + item.suffix + '] ' + item.name
            
            displaystr += '\n'
            
            if i >= self.minScrollPos and i <= self.maxScrollPos :
                if item.hovered :
                    self.window.addstr(1 + i, 1, displaystr, curses.A_STANDOUT)
                else :
                    self.window.addstr(1 + i, 1, displaystr)
            
            i += 1
        

    def refresh(self):
        self.redraw(self.nlines, self.ncols, self.posY, self.posX)

class gui():
    
    def initCurses(self):
        self.screen = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(1)

        selector = Selector([Item('hello.png'), Item('whatsup.d'), Item('config.py')])
        self.inptwin = InputWindow(curses.LINES, curses.COLS)
        self.dirwin = SelectorWindow(curses.LINES - 3, curses.COLS - 2, 1, 1)
        self.dirwin.addSelector(selector)
        self.inptwin.refresh()
        self.dirwin.refresh()

    def startGui(self):
        self.initCurses()
        escape = False



        while not escape:


            
            x = self.inptwin.window.getch()

            if x == ord("q"):
                escape = True
                curses.endwin()
            elif x == curses.KEY_RESIZE:
                #the order these functions get called is vital
                self.screen.refresh()
                maxY, maxX = self.screen.getmaxyx()
                self.dirwin.redraw(maxY-3, maxX-2, 1, 1)
                self.inptwin.redraw(maxY, maxX)
            else :
                self.inptwin.addinput(str(x))
                self.inptwin.refresh()
#g = gui()
#g.startGui()
