#!/usr/bin/env python
 
import curses
import curses.textpad
 
 
stdscr = curses.initscr()
 
words = ''
 
 
def mywin():
    global words
    
    stdwin = curses.newwin(1,curses.COLS,curses.LINES-1,0)
    stdwin2 = curses.newwin(1000, curses.COLS, 0, 0)
 
    lines = 0
    while True:
        stdwin.addstr('#>')
        stdwin.refresh()
        while True:
            k = stdwin.getkey()
            if k != '\n':
                words += k
            else:
                stdwin2.addstr(words + '\n')
                stdwin2.refresh()
                lines += int(len(words) / curses.COLS) + 1 
                if lines >= curses.LINES-2:
                    stdwin2.clear()
                    lines = int(len(words) / curses.COLS) + 1
                words=''
                stdwin.clear()
                break
 
try:
    mywin()
except Exception:
    raise Exception
finally:
    curses.endwin()
