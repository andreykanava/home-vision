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

def telegram_send_message(message):
    bot = telebot.TeleBot(TOKEN)
    bot.send_message(CHAT_ID, message)

def run_check_connection():
    asyncio.run(check_connection())

def main_network(stdscr):
    from screens.start_menu import main_screen
    from screens.schedule.main_screen import main_schedule

    while True:
        stdscr.clear()
        stdscr.nodelay(True)
        text_ui.add_text(stdscr, align.center_vertical, f'Enter network password', row=-3)
        text_ui.add_text(stdscr, align.center_vertical, f'‾ ‾ ‾ ‾', row=1)
        text_ui.add_text(stdscr, align.center_vertical, f'Back', row=5, color=curses.COLOR_BLACK, background=curses.COLOR_WHITE)
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
        if entered_keys == [50, 56, 49, 50]:
            text_ui.add_text(stdscr, align.center_vertical, f'connecting', row=4)
            subprocess.run(["sudo", "systemctl", "start", "parprouted"])
            telegram_send_message("Успешно введен пароль, подключение...")
            asyncio_thread = threading.Thread(target=run_check_connection)
            asyncio_thread.start()
            curses.wrapper(main_schedule)


        elif len(entered_keys) == 4 and entered_keys != [50, 56, 49, 50]:
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
            time.sleep(0.1)
