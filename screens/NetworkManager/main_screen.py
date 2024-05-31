import curses
from utils import align, menu_track
from components.menu import menu_ui
from components.text import text_ui
from screens.NetworkManager.network_util import check_connection, TOKEN, CHAT_ID
from datetime import datetime
import time
import telebot
import asyncio
import subprocess
from curses import KEY_ENTER
import threading
import RPi.GPIO as GPIO

def telegram_send_message(message):
    bot = telebot.TeleBot(TOKEN)
    bot.send_message(CHAT_ID, message)

def run_check_connection():
    asyncio.run(check_connection())

def main_network(stdscr):
    from screens.start_menu import main_screen
    from screens.schedule.main_screen import main_schedule

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

    #            ^` ^l      ^o  ^e ^`           ^o  ^a   ^a ^b   ^o     ^o             
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
                    pressed_key = char
                    key_states[char] = True
            else:
                key_states[char] = False
        GPIO.output(line, GPIO.LOW)
        return pressed_key
    time.sleep(0.3)
    while True:
        stdscr.clear()
        stdscr.nodelay(True)
        text_ui.add_text(stdscr, align.center_vertical, f'Enter network password', row=-3)
        text_ui.add_text(stdscr, align.center_vertical, f'‾ ‾ ‾ ‾', row=1)
        text_ui.add_text(stdscr, align.center_vertical, f'Back (S16)', row=5, color=curses.COLOR_BLACK, background=curses.COLOR_WHITE)
        try:
            if entered_keys:
                pass
        except:
             entered_keys = []
        try:
            if try_again:
                pass
        except:
            try_again = False
        #text_ui.add_text(stdscr, align.center_vertical, f'{entered_keys}', row=2)
        if entered_keys == [50, 56, 49, 50] or entered_keys == ["2", "8", "1", "2"]:
            text_ui.add_text(stdscr, align.center_vertical, f'connecting', row=4)
            subprocess.run(["sudo", "systemctl", "start", "parprouted"])
            telegram_send_message("Успешно введен пароль, подключение служб.")
            asyncio_thread = threading.Thread(target=run_check_connection)
            asyncio_thread.start()
            GPIO.cleanup()
            curses.wrapper(main_schedule)


        elif len(entered_keys) == 4 and entered_keys != [50, 56, 49, 50] or len(entered_keys) == 4 and entered_keys != ["2", "8", "1", "2"]:
            telegram_send_message(f"Неправильная попытка ввода пароля!")
            entered_keys = []
        if len(entered_keys) <= 4:
            stars = []
            for i in range(len(entered_keys)):
                stars.append("*")

            lable = " ".join(stars)
            text_ui.add_text(stdscr, align.center_vertical, lable, row=0)

            key = stdscr.getch()
            if key == ord("1") or key == ord("2") or key == ord("3") or key == ord("4") or key == ord("5") or key == ord("6") or key == ord("7") or key == ord("8") or key == ord("9"):
                entered_keys.append(key)
            else:
                if key == KEY_ENTER or key in [10, 13]:
                    curses.wrapper(main_screen)
            
            pressed_key = None
            pressed_key = readLine(L1, ["1", "2", "3", "A"]) or pressed_key
            pressed_key = readLine(L2, ["4", "5", "6", "B"]) or pressed_key
            pressed_key = readLine(L3, ["7", "8", "9", "C"]) or pressed_key
            pressed_key = readLine(L4, ["*", "0", "#", "D"]) or pressed_key
            if pressed_key is not None:
                if pressed_key == "D":
                    GPIO.cleanup()
                    curses.wrapper(main_screen)

                entered_keys.append(pressed_key)

            time.sleep(0.1)
