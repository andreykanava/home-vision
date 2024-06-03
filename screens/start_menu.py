import curses
from utils import align, menu_track
from components.menu import menu_ui
from components.text import text_ui
#from screens.wifi_scanner.interface_choose_screen import interface_choose_screen
from screens.schedule.main_screen import choose
from screens.NetworkManager.main_screen import main_network
from screens.VPN.main_screen import action
import time
import RPi.GPIO as GPIO
from curses import KEY_UP, KEY_DOWN, KEY_ENTER

def main_screen(stdscr):
    stdscr.clear()
    curses.curs_set(0)

    list = ["Main", "Network Manager", "VPN", "Exit to terminal"]

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
                GPIO.cleanup()
                curses.wrapper(choose)
                pass
            elif selected_last == 1:
                GPIO.cleanup()
                curses.wrapper(main_network)
                pass
            elif selected_last == 2:
                GPIO.cleanup()
                curses.wrapper(action)
                pass
            elif selected_last == 3:
                GPIO.cleanup()
                exit()
        else:
            stdscr.clear()
            menu_ui.scroll_menu(stdscr, align.center_vertical, list, 5, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
            selected_last = selected
            time.sleep(0.1)
    