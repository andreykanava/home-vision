import curses
from utils import align, menu_track
from components.menu import menu_ui
from components.text import text_ui
from screens.wifi_scanner import scanner_utils
from screens.wifi_scanner.scanner_screen import scanner_screen

def interface_choose_screen(stdscr):
    from screens.start_menu import main_screen

    stdscr.clear()
    curses.curs_set(0)

    interfaces = scanner_utils.get_network_interfaces()  + ["Go back"]

    if len(interfaces) == 1:
        text_ui.add_text(align.center_vertical, "No wifi interfaces were found!", -3)
        menu_ui.menu(stdscr, align.center_vertical, ["Go back"], curses.COLOR_BLACK, curses.COLOR_WHITE)
        while 1:
            selected = menu_track.menu_select(stdscr, ["Go back"], selected)
            if selected == "Enter":
                curses.wrapper(main_screen)

    selected = 0
    selected_last = 0

    menu_ui.scroll_menu(stdscr, align.center_vertical, interfaces, 5, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)   
    stdscr.refresh()

    while 1:
        selected = menu_track.menu_select(stdscr, interfaces, selected)
        if selected == "Enter":
            if selected_last == len(interfaces)-1:
                curses.wrapper(main_screen)
            else:
                curses.wrapper(scanner_screen(stdscr, interfaces[selected_last]))
        else:
            stdscr.clear()
            menu_ui.scroll_menu(stdscr, align.center_vertical, interfaces, 5, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
            selected_last = selected