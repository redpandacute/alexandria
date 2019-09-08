import curses
import threading
import os

class gui():
    
    def initCurses(self):
        self.screen = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(1)

        self.inptwin = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)
        self.inptwin.addstr(':>')

    def startGui(self):
        self.initCurses()

        escape = False
        while not escape:
            maxY, maxX = self.screen.getmaxyx()
            #maxiY, maxiY = self.inptwin.getmaxyx()
            #self.screen.border('|', '|', '-','-', '>', '<', '>','<')
            #self.screen.addstr("this is the screen window")
            #self.inptwin = curses.newwin(1, maxX, maxY - 1, 0)
            #self.inptwin.addstr(":>")
            self.inptwin.mvwin(maxY - 1, 0)
            self.inptwin.resize(1, maxX)
            self.inptwin.border('=','=','=','=','=','=','=','=')
            self.inptwin.refresh()
            x = self.inptwin.getch()

            if x == ord("q"):
                escape = True
                curses.endwin()
            elif x == curses.KEY_RESIZE:
                #self.screen.erase()
                #self.inptwin.erase()
                #self.inptwin.clrtobot()
                self.inptwin.refresh()
                self.screen.refresh()


g = gui()
g.startGui()
