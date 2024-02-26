import curses
from utils import align, menu_track
from components.menu import menu_ui
from components.text import text_ui
from screens.wifi_scanner import scanner_utils

def scanner_screen(stdscr, interface):
    from screens.wifi_scanner.interface_choose_screen import interface_choose_screen
    stdscr.clear()
    curses.curs_set(0)
    text_ui.add_text(stdscr, align.center_vertical, f"scanning on interface: {interface}", row=-4)


    wifis = scanner_utils.scan_wifi_networks(interface)

    for i in wifis:
        text_ui.add_text(stdscr, align.center_vertical, i)


    selected = 0
    selected_last = 0

    menu_ui.menu(stdscr, align.center_vertical, ["Go back"], curses.COLOR_BLACK, curses.COLOR_WHITE, row=len(wifis)+3)
    while 1:
        selected = menu_track.menu_select(stdscr, ["Go back"], selected)
        if selected == "Enter":
            curses.wrapper(interface_choose_screen)