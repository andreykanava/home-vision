import curses
from utils import align, menu_track
from components.menu import menu_ui
from components.text import text_ui
from screens.tests.test_text import text_screen
import time

def menu_screen(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    list = ["opt1", "opt2", "opt3"]
    selected = 0
    selected_last = 0
    text_ui.add_text(stdscr, align.center_vertical, str(selected), row=-3,  color=curses.COLOR_BLACK, background=curses.COLOR_WHITE) 
    menu_ui.menu(stdscr, align.center_vertical, list, curses.COLOR_BLACK, curses.COLOR_WHITE, selected) 
    stdscr.refresh()
    while 1:
        selected = menu_track.menu_select(stdscr, list, selected)
        if selected == "Enter":
            curses.wrapper(text_screen(stdscr, text=f"Selected: {selected_last}"))
            break
        else:
            text_ui.add_text(stdscr, align.center_vertical, str(selected), row=-3) 
            menu_ui.menu(stdscr, align.center_vertical_vertical, list, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
            selected_last = selected
    