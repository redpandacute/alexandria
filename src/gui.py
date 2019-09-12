import curses
import threading
import os
import window
from modes import GlobalMode
from modes import NavMode

class gui():

    screen = None
    inptwin = None
    originPath = None
    dirwinHandler  = None
    
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
        self.dirwinHandler = DirWinHandler('./', curses.LINES - 3, curses.COLS - 1, 1,1)
        self.setMode(GlobalMode.NAVIGATION_MODE)

    def startGui(self):


        self.initCurses()
        escape = False

        while not escape:

            x = self.inptwin.window.getch()

            #global input reactions
            if x == ord("q"):
                escape = True
                curses.endwin()
            elif x == curses.KEY_RESIZE:
                #the order these functions get called is vital
                self.screen.refresh()
                maxY, maxX = self.screen.getmaxyx()
                self.dirwinHandler.redraw(maxY-3, maxX-1, 1, 1)
                self.inptwin.redraw(maxY, maxX)
            else :
                #Modeswaps
                if not self.mode == GlobalMode.COMMAND_MODE and x == ord(':') :
                    self.setMode(GlobalMode.COMMAND_MODE)
                elif not self.mode == GlobalMode.NAVIGATION_MODE and x == 27 :
                    self.setMode(GlobalMode.NAVIGATION_MODE)
                
                else:
                    #determine the reactor
                    if self.mode == GlobalMode.NAVIGATION_MODE :
                        self.dirwinHandler.react(x)

                    elif self.mode == GlobalMode.COMMAND_MODE :
                        self.inptwin.react(x)
                    else:
                        pass

    def setMode(self, mode):
        if mode == GlobalMode.COMMAND_MODE:
            self.mode = GlobalMode.COMMAND_MODE
            self.inptwin.flush()
            self.inptwin.addinput(':')
            self.inptwin.refresh()
            curses.curs_set(1) #enabling cursor 
        
        elif mode == GlobalMode.NAVIGATION_MODE:
            self.mode = GlobalMode.NAVIGATION_MODE
            curses.curs_set(0) #getting rid of the cursor

class DirWinHandler():
    
    originPath = ''
    dirWindows = []
    screen = None
    openDisplayWin = False

    def __init__(self, originPath, nlines, ncols, posY, posX):
        self.focused = True #provisorisch
        self.nlines = nlines
        self.ncols = ncols
        self.posY = posY
        self.posX = posX
        self.originPath = originPath
        self.originDirWindow = window.SelectorWindow(self.originPath, nlines, ncols, posY, posX)
        self.dirWindows.append(self.originDirWindow)
        
        self.openWindow = self.originDirWindow
        #self.openWindow.focused = True
        self.dirWindows[0].focused = True
        
        self.depth = 0
        self.refresh()

    def addWindow(self, path):
        self.dirWindows.append(window.SelectorWindow(path))

    def removeLastWindow(self):
        del self.dirWindows[-1]

    def redraw(self, new_nlines, new_ncols, new_posY, new_posX):
        self.ncols = new_ncols
        self.nlines = new_nlines
        self.posY = new_posY
        self.posX = new_posX

        if self.openDisplayWin:
            pass #implement displayWin
        else:
            spaceunit = (self.ncols) // (len(self.dirWindows) + 2) - 1#-1 gets added afterwards due to spacing

            i = 0
            for window in self.dirWindows:
                if i > 0:
                    posX = (spaceunit + 1) * i - i
                else:
                    posX = (spaceunit + 1) * i

                if window.focused :
                    window.redraw(self.nlines, spaceunit * 3, self.posY, posX)
                    i += 2
                else:
                    window.redraw(self.nlines, spaceunit, self.posY, posX)
                i += 1

            #fills up potential errors with the // operation
            self.dirWindows[-1].redraw(
                    self.dirWindows[-1].nlines,
                    self.dirWindows[-1].ncols + (self.ncols - i * (spaceunit + 1)) + i,
                    self.dirWindows[-1].posY,
                    self.dirWindows[-1].posX
            )
            self.dirWindows[-1].refresh()

    def refresh(self):
        self.redraw(self.nlines, self.ncols, self.posY, self.posX)

    
    def react(self, key):
        if self.focused:
           
            #unperformable on an empty window
            if not self.openWindow.empty:
                if key == ord('o'):
                    self.openWindow.down()
                    return
                if key == ord(','):
                    self.openWindow.up()
                    return
                if key == ord('e'):
                    self.open(self.openWindow.currentItem())
                    return
                if key == ord(' '):
                    self.openWindow.select(self.openWindow.currentIndex)
                    return
            if key == ord('a'):
                self.close()
                return


    def open(self, item):
        if item.isDir:
            self.depth += 1
            self.addWindow(self.openWindow.dirPath + item.name + '/')
            self.openWindow.focused = False
            self.dirWindows[-1].focused = True
            self.openWindow = self.dirWindows[-1]
            self.refresh()
        else:
            #TODO: implement preview option maybe
            pass

    def close(self):
        if self.depth > 0:
            self.depth -= 1
            self.removeLastWindow()
            self.openWindow = self.dirWindows[-1]
            self.dirWindows[-1].focused = True
            self.refresh()
        else:
            pass

g = gui()
curses.wrapper(g.startGui())
