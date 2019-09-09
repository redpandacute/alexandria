import curses

class InputWindow():
    

    PROMPT = ':-:'
    inputstr = ''

    def __init__(self, maxY, maxX):
        self.maxY = maxY
        self.maxX = maxX
        self.window = curses.newwin(1, self.maxX - 2, self.maxY - 1, 1)
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
        self.window.mvwin(self.maxY - 1, 1)

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

    def __init__(self, nlines, ncols, posY,  posX):
        self.ncols = ncols
        self.nlines = nlines
        self.posY = posY
        self.posX = posX
        self.window = curses.newwin(self.nlines, self.ncols, self.posY, self.posX)
        #self.window = screen.subwin(nlines, self.ncols, self.posY, self.posX)

    def redraw(self, new_nlines, new_ncols, new_posY, new_posX):
        global window
        global ncols
        global nlines
        global posY
        global posX

        self.nlines = new_nlines
        self.ncols = new_ncols
        self.posY = new_posY
        self.posX = new_posX
        self.window.clear()
        self.window.refresh()
        self.window.resize(self.nlines, self.ncols) 
        self.window.mvwin(new_posY, new_posX)
        self.window.border('|', '|', '-','-', '>', '<', '>','<')
        self.window.refresh()

    def refresh(self):
        self.redraw(self.nlines, self.ncols, self.posY, self.posX)

class gui():
    
    def initCurses(self):
        self.screen = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(1)

        self.inptwin = InputWindow(curses.LINES, curses.COLS)
        self.dirwin = SelectorWindow(curses.LINES - 3, curses.COLS - 2, 1, 1)
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
                #dont change the arrangement of these 3 functions
                self.screen.refresh()
                maxY, maxX = self.screen.getmaxyx()

                self.dirwin.redraw(maxY-3, maxX-2, 1, 1)
                self.inptwin.redraw(maxY, maxX)
            else :
                self.inptwin.addinput(str(x))
                self.inptwin.refresh()
g = gui()
g.startGui()
