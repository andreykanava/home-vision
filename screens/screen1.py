import curses
from utils import align, menu_track
from components.menu import menu_ui
from components.text import text_ui

def menu_screen1(stdscr):
    from screens.start_menu import main_screen
    from screens.screen2 import menu_screen2
    stdscr.clear()
    curses.curs_set(0)
    
    list = ["Menu", "Screen 2"]

    selected = 0
    selected_last = 0

    menu_ui.menu(stdscr, align.left_vertical, list, curses.COLOR_BLACK, curses.COLOR_WHITE, selected) 
    stdscr.refresh()

    while 1:
        selected = menu_track.key_track(stdscr, list, selected)
        if selected == "Enter":
            if selected_last == 0:
                curses.wrapper(main_screen)
            elif selected_last == 1:
                curses.wrapper(menu_screen2(stdscr))
                
        else:
            menu_ui.menu(stdscr, align.left_vertical, list, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
            selected_last = selected
    