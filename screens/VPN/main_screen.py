import time
from screens.VPN.vpn_utils import connect_vpn, disconnect_vpn
from pathlib import Path
from utils import align, menu_track
from components.menu import menu_ui
from components.text import text_ui
import curses
import RPi.GPIO as GPIO
from curses import KEY_UP, KEY_DOWN, KEY_ENTER

def action(stdscr):
    from screens.start_menu import main_screen
    stdscr.clear()
    curses.curs_set(0)

    list = ["Connect", "Disconnect", "Back"]

    selected = 0
    selected_last = 0

    menu_ui.scroll_menu(stdscr, align.center_vertical, list, 5, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
    stdscr.refresh()

    
    L1 = 5
    L2 = 6
    L3 = 13
    L4 = 19

    C1 = 12
    C2 = 16
    C3 = 20
    C4 = 21

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(L3, GPIO.OUT)
    GPIO.setup(L4, GPIO.OUT)

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            
    key_states = {
        '1': False, '2': False, '3': False, 'A': False,
        '4': False, '5': False, '6': False, 'B': False,
        '7': False, '8': False, '9': False, 'C': False,
        '*': False, '0': False, '#': False, 'D': False
    }
    def readLine(line, characters):
        pressed_key = None
        GPIO.output(line, GPIO.HIGH)
        for i, char in enumerate(characters):
            if GPIO.input([C1, C2, C3, C4][i]) == 1:
                if not key_states[char]:
                    print(char)
                    pressed_key = char
                    key_states[char] = True
            else:
                key_states[char] = False
        GPIO.output(line, GPIO.LOW)
        return pressed_key


    time.sleep(0.3)

    while True:
        
        pressed_key = None
        pressed_key = readLine(L1, ["1", "2", "3", "A"]) or pressed_key
        pressed_key = readLine(L2, ["4", "5", "6", "B"]) or pressed_key
        pressed_key = readLine(L3, ["7", "8", "9", "C"]) or pressed_key
        pressed_key = readLine(L4, ["*", "0", "#", "D"]) or pressed_key
        if pressed_key is not None:
            if pressed_key == "2":
                key = KEY_UP
            elif pressed_key == "5":
                key = KEY_ENTER
            elif pressed_key == "8":
                key = KEY_DOWN
            elif pressed_key == "D":
                GPIO.cleanup()
                curses.wrapper(main_screen)
            else:
                key = stdscr.getch()
        else:
            key = stdscr.getch()

        if key == KEY_UP and selected > 0:
            selected = selected - 1
        elif key == KEY_UP and selected == 0:
            selected = len(list)-1
        elif key == KEY_DOWN and selected < len(list)-1:
            selected = selected + 1
        elif key == KEY_DOWN and selected == len(list) -1:
            selected = 0
        elif key == KEY_ENTER or key in [10, 13]:
            selected = "Enter"
        else:
            selected = selected

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



    L1 = 5
    L2 = 6
    L3 = 13
    L4 = 19

    C1 = 12
    C2 = 16
    C3 = 20
    C4 = 21

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(L3, GPIO.OUT)
    GPIO.setup(L4, GPIO.OUT)

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            
    key_states = {
        '1': False, '2': False, '3': False, 'A': False,
        '4': False, '5': False, '6': False, 'B': False,
        '7': False, '8': False, '9': False, 'C': False,
        '*': False, '0': False, '#': False, 'D': False
    }
    def readLine(line, characters):
        pressed_key = None
        GPIO.output(line, GPIO.HIGH)
        for i, char in enumerate(characters):
            if GPIO.input([C1, C2, C3, C4][i]) == 1:
                if not key_states[char]:
                    print(char)
                    pressed_key = char
                    key_states[char] = True
            else:
                key_states[char] = False
        GPIO.output(line, GPIO.LOW)
        return pressed_key



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
        

        pressed_key = None
        pressed_key = readLine(L1, ["1", "2", "3", "A"]) or pressed_key
        pressed_key = readLine(L2, ["4", "5", "6", "B"]) or pressed_key
        pressed_key = readLine(L3, ["7", "8", "9", "C"]) or pressed_key
        pressed_key = readLine(L4, ["*", "0", "#", "D"]) or pressed_key
        if pressed_key is not None:
            if pressed_key == "2":
                key = KEY_UP
            elif pressed_key == "5":
                key = KEY_ENTER
            elif pressed_key == "8":
                key = KEY_DOWN
            elif pressed_key == "D":
                GPIO.cleanup()
                curses.wrapper(main_screen)
            else:
                key = stdscr.getch()
        else:
            key = stdscr.getch()

        if key == KEY_UP and selected > 0:
            selected = selected - 1
        elif key == KEY_UP and selected == 0:
            selected = len(files)-1
        elif key == KEY_DOWN and selected < len(files)-1:
            selected = selected + 1
        elif key == KEY_DOWN and selected == len(files) -1:
            selected = 0
        elif key == KEY_ENTER or key in [10, 13]:
            selected = "Enter"
        else:
            selected = selected
        time.sleep(0.1)


        if selected == "Enter":
            config_name = files[selected_last]
            text_ui.add_text(stdscr, align.center_vertical, f'connecting', row=8)
            connect_vpn(f'/home/pi/home-vision/screens/VPN/configs/{config_name}.ovpn', '/home/pi/home-vision/screens/VPN/credentials.txt')
            time.sleep(2)
            GPIO.cleanup()
            curses.wrapper(main_screen)
        else:
            stdscr.clear()
            menu_ui.scroll_menu(stdscr, align.center_vertical, files, 7, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
            selected_last = selected
        time.sleep(0.1)
        

