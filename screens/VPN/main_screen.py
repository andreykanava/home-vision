import time
from screens.VPN.vpn_utils import connect_vpn, disconnect_vpn
from pathlib import Path
from utils import align, menu_track
from components.menu import menu_ui
from components.text import text_ui
import curses

def action(stdscr):
    from screens.start_menu import main_screen
    stdscr.clear()
    curses.curs_set(0)

    list = ["Connect", "Disconnect", "Back"]

    selected = 0
    selected_last = 0

    menu_ui.scroll_menu(stdscr, align.center_vertical, list, 5, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
    stdscr.refresh()

    while True:
        selected = menu_track.menu_select(stdscr, list, selected)
        if selected == "Enter":
            if selected_last == 0:
                curses.wrapper(choose_vpn)
                pass
            elif selected_last == 1:
                disconnect_vpn()
                curses.wrapper(main_screen)
                pass
            elif selected_last == 2:
                curses.wrapper(main_screen)
                pass
        else:
            stdscr.clear()
            menu_ui.scroll_menu(stdscr, align.center_vertical, list, 5, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
            selected_last = selected

def choose_vpn(stdscr):
    from screens.start_menu import main_screen
    stdscr.clear()
    stdscr.nodelay(True)
    folder_path = Path('/home/pi/home-vision/screens/VPN/configs/')
    files = [f.stem for f in folder_path.glob('*.ovpn')]
    files = sorted(files)

    selected = 0
    selected_last = 0

    menu_ui.scroll_menu(stdscr, align.center_vertical, files, 7, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
    line = "db    db d8888b. d8b   db "
    text_ui.add_text(stdscr, align.center_vertical, line, row=-11)
    line = "88    88 88  `8D 888o  88 "
    text_ui.add_text(stdscr, align.center_vertical, line, row=-10)
    line = "Y8    8P 88oodD' 88V8o 88 "
    text_ui.add_text(stdscr, align.center_vertical, line, row=-9)
    line = "`8b  d8' 88~~~   88 V8o88 "
    text_ui.add_text(stdscr, align.center_vertical, line, row=-8)
    line = " `8bd8'  88      88  V888 "
    text_ui.add_text(stdscr, align.center_vertical, line, row=-7)
    line = "   YP    88      VP   V8P "
    text_ui.add_text(stdscr, align.center_vertical, line, row=-6)
    text_ui.add_text(stdscr, align.center_vertical, "Back S16", row=10)
    stdscr.refresh()

    time.sleep(0.3)
    while True:
        line = "db    db d8888b. d8b   db "
        text_ui.add_text(stdscr, align.center_vertical, line, row=-11)
        line = "88    88 88  `8D 888o  88 "
        text_ui.add_text(stdscr, align.center_vertical, line, row=-10)
        line = "Y8    8P 88oodD' 88V8o 88 "
        text_ui.add_text(stdscr, align.center_vertical, line, row=-9)
        line = "`8b  d8' 88~~~   88 V8o88 "
        text_ui.add_text(stdscr, align.center_vertical, line, row=-8)
        line = " `8bd8'  88      88  V888 "
        text_ui.add_text(stdscr, align.center_vertical, line, row=-7)
        line = "   YP    88      VP   V8P "
        text_ui.add_text(stdscr, align.center_vertical, line, row=-6)

        text_ui.add_text(stdscr, align.center_vertical, "Back S16", row=10)
        selected = menu_track.menu_select(stdscr, files, selected)
        if selected == "Enter":
            config_name = files[selected_last]
            text_ui.add_text(stdscr, align.center_vertical, f'connecting', row=8)
            connect_vpn(f'configs/{config_name}.ovpn', 'credentials.txt')
            time.sleep(3)
            curses.wrapper(main_screen)
        else:
            stdscr.clear()
            menu_ui.scroll_menu(stdscr, align.center_vertical, files, 7, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
            selected_last = selected
        time.sleep(0.1)
        

