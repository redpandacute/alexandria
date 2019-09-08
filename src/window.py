import curses


class InputWindow():
    

    PROMPT = ':-:'
    inputstr = ''

    def __init__(self, maxY, maxX):
        self.maxY = maxY
        self.maxX = maxX
        self.window = curses.newwin(1, maxX, maxY - 1, 0)
        #self.window.addstr(self.PROMPT + self.inputstr)
        #self.window.border('|', '|', '-','-', '>', '<', '>','<')
    
    def redraw(self, new_maxY, new_maxX):
        global window
        global maxY
        global maxX

        self.maxY = new_maxY
        self.maxX = new_maxX
        self.window.mvwin(self.maxY - 1, 0)
        self.window.resize(1, self.maxX)    
        self.window.border('|', '|', '-','-', '>', '<', '>','<')
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


class gui():
    
    def initCurses(self):
        self.screen = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(1)

        self.inptwin = InputWindow(curses.LINES, curses.COLS)
        self.inptwin.refresh()

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
                self.inptwin.redraw(maxY, maxX)
g = gui()
g.startGui()
