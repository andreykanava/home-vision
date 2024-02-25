import curses
from utils import align, menu_track
from components.menu import menu_ui
from components.text import text_ui
from screens import screen1, screen2

def main_screen(stdscr):
    stdscr.clear()
    curses.curs_set(0)

    list = ["Screen 1", "Screen 2", "Exit to terminal"]

    selected = 0
    selected_last = 0

    text_ui.add_text(stdscr, align.center_vertical, "HACKVERSITY", row=-8,  color=curses.COLOR_BLACK, background=curses.COLOR_WHITE)
    menu_ui.menu(stdscr, align.left_vertical, list, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
    stdscr.refresh()

    while 1:
        selected = menu_track.key_track(stdscr, list, selected)
        if selected == "Enter":
            if selected_last == 0:
                curses.wrapper(screen1.menu_screen1(stdscr))
            elif selected_last == 1:
                curses.wrapper(screen2.menu_screen2(stdscr))
            elif selected_last == 2:
                exit()
        else:
            menu_ui.menu(stdscr, align.left_vertical, list, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
            selected_last = selected
    