import curses
from utils import align
from components.text import text_ui
import time

def text_screen(stdscr, text):
    while True:
        stdscr.clear()
        curses.curs_set(0)
        text2 = "Line 2"
        text_ui.add_text(stdscr, align.center_vertical, text) 
        #text_ui.add_text(stdscr, align.center_vertical, text2, row=-3)
        stdscr.refresh()
        time.sleep(1)

    