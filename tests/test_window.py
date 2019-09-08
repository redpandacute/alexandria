import curses
import os

VERSION = "0.1-dev" #version number

screen = curses.initscr() #initialize the curses window

#Configure color pairs for showing select menu options as highlighted
curses.start_color() #enable color for highlighting menu options
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) #color pair 1
highlightText = curses.color_pair(1) #color pair for highlighted menu option
normalText = curses.A_NORMAL #color pair for non-highlighted menu options

#Configure global variables for Curses
curses.noecho() #disable the keypress echo to prevent double input
curses.cbreak() #disable line buffers to run the keypress immediately
curses.curs_set(0)
screen.keypad(1) #enable keyboard use
screen.addstr(2, 2, "Screen Resize Test" + VERSION, curses.A_UNDERLINE)

#test screen resize
def main_screen():
    escape = False
    while escape == False:
        maxY, maxX = screen.getmaxyx()
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')
        screen.addstr(4, 2, "MaxY: " + str(maxY))
        screen.addstr(5, 2, "MaxX: " + str(maxX))

        x = screen.getch()

        if x == ord("q"):
            escape = True
            curses.endwin()
        elif x == curses.KEY_RESIZE:
            screen.erase()
            screen.addstr(2, 2, "Screen Resize Test" + VERSION, curses.A_UNDERLINE)

main_screen()
