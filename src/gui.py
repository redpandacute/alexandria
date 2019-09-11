import curses
import threading
import os
import window

class gui():

    screen = None
    inptwin = None
    originPath = None
    dirwinHandler  = None

    focus = inptwin
    
    def initCurses(self):
        global screen
        global inputwindow
        global dirwindows

        self.screen = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(1)

        self.inptwin = window.InputWindow(curses.LINES, curses.COLS)
        self.dirwinHandler = DirWinHandler('./', curses.LINES - 3, curses.COLS - 2, 1,1)
        
    def startGui(self):


        self.initCurses()
        escape = False

        while not escape:

            x = self.inptwin.window.getch()

            if x == ord("q"):
                escape = True
                curses.endwin()
            elif x == ord("a"):
                self.dirwinHandler.addWindow('./__pycache__/')
            elif x == curses.KEY_RESIZE:
                #the order these functions get called is vital
                self.screen.refresh()
                maxY, maxX = self.screen.getmaxyx()
                self.dirwinHandler.redraw(maxY-3, maxX-2, 1, 1)
                self.inptwin.redraw(maxY, maxX)
            else :
                self.inptwin.addinput(str(x))
                self.inptwin.refresh()

class DirWinHandler():
    
    originPath = ''
    dirWindows = []
    screen = None
    openDisplayWin = False

    def __init__(self, originPath, nlines, ncols, posY, posX):

        self.nlines = nlines
        self.ncols = ncols
        self.posY = posY
        self.posX = posX
        self.originPath = originPath
        self.originDirWindow = window.SelectorWindow(os.listdir(originPath), nlines, ncols, posY, posX)
        self.dirWindows.append(self.originDirWindow)
        self.refresh()

    def addWindow(self, path):
        self.dirWindows.append(window.SelectorWindow(os.listdir(path)))
        self.refresh()

    def redraw(self, new_nlines, new_ncols, new_posY, new_posX):
        self.ncols = new_ncols
        self.nlines = new_nlines
        self.posY = new_posY
        self.posX = new_posX

        if self.openDisplayWin:
            pass #implement displayWin
        else:
            spaceunit = self.ncols // (len(self.dirWindows) + 2)#-1 gets added afterwards due to spacing

            i = 0
            for window in self.dirWindows:
                if window.focused :
                    window.redraw(self.nlines, spaceunit * 3 + 2, self.posY, spaceunit * i + i)
                    i += 1
                else:
                    window.redraw(self.nlines, spaceunit + 1, self.posY, spaceunit * i + i)
                i += 1

            #using up the space if no dirwin is focused
            if i - len(self.dirWindows) == 0:
                self.dirWindows[len(self.dirWindows) - 1].redraw(self.nlines, spaceunit * 3 + 2, self.posY, spaceunit * (i - 1))
                self.dirWindows[len(self.dirWindows) - 1].refresh()
        
    def refresh(self):
        self.redraw(self.nlines, self.ncols, self.posY, self.posX)
        

g = gui()
curses.wrapper(g.startGui())
