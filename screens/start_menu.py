import curses
from utils import align, menu_track
from components.menu import menu_ui
from components.text import text_ui
#from screens.wifi_scanner.interface_choose_screen import interface_choose_screen
from screens.schedule.main_screen import main_schedule

def main_screen(stdscr):
    stdscr.clear()
    curses.curs_set(0)

    list = ["Main", "Exit to terminal"]

    selected = 0
    selected_last = 0

    menu_ui.scroll_menu(stdscr, align.center_vertical, list, 5, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
    stdscr.refresh()

    while 1:
        selected = menu_track.menu_select(stdscr, list, selected)
        if selected == "Enter":
            if selected_last == 0:
                curses.wrapper(main_schedule)
            elif selected_last == 1:
                exit()
        else:
            stdscr.clear()
            menu_ui.scroll_menu(stdscr, align.center_vertical, list, 5, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
            selected_last = selected
    