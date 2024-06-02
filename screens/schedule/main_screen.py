import curses
from utils import align, menu_track
from components.menu import menu_ui
from components.text import text_ui
from screens.schedule.schedule_utlis import getschedule, current_event, next_event, get_weather_forecast
from datetime import datetime
import time
import asyncio
import subprocess
from pyfiglet import Figlet
import RPi.GPIO as GPIO

def is_midnight():
    # Получаем текущее время
    current_time = datetime.now()
    
    # Проверяем, что часы и минуты равны 00:00
    if current_time.hour == 0 and current_time.minute == 0:
        return True
    else:
        return False

def ping(host):
    """
    Пингует указанный хост и возвращает True, если хост доступен, иначе False.
    
    :param host: IP-адрес или имя хоста для пинга.
    :return: True если хост доступен, False иначе.
    """
    try:
        # Выполняем команду ping, результат сохраняем в переменной
        output = subprocess.run(["ping", "-c", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Проверяем код возврата
        if output.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        # В случае исключения возвращаем False
        print(f"Ошибка при попытке выполнить команду ping: {e}")
        return False

    
def choose(stdscr):
    from screens.start_menu import main_screen
    stdscr.clear()
    curses.curs_set(0)

    list = ["Lessons", "Forecast", "Back"]

    selected = 0
    selected_last = 0

    menu_ui.scroll_menu(stdscr, align.center_vertical, list, 5, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
    stdscr.refresh()

    while True:
        selected = menu_track.menu_select(stdscr, list, selected)
        if selected == "Enter":
            if selected_last == 0:
                curses.wrapper(main_schedule)
                pass
            elif selected_last == 1:
                curses.wrapper(main_forecast)
                pass
            elif selected_last == 2:
                curses.wrapper(main_screen)
                pass
        else:
            stdscr.clear()
            menu_ui.scroll_menu(stdscr, align.center_vertical, list, 5, curses.COLOR_BLACK, curses.COLOR_WHITE, selected)
            selected_last = selected

def main_schedule(stdscr):
    from screens.start_menu import main_screen

    timetable = {
        1: ["8:10", "8:55"],
        2: ["9:00", "9:45"],
        3: ["9:50", "10:35"],
        4: ["10:45", "11:30"],
        5: ["12:00", "12:45"],
        6: ["12:55", "13:40"],
        7: ["13:50", "14:35"],
        8: ["14:45", "15:30"]
    }
    timetable_print = {
        1: ["8:10", "8:55  "],
        2: ["9:00", "9:45  "],
        3: ["9:50", "10:35 "],
        4: ["10:45", "11:30"],
        5: ["12:00", "12:45"],
        6: ["12:55", "13:40"],
        7: ["13:50", "14:35"],
        8: ["14:45", "15:30"]
    }

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
                    print(char)
                    pressed_key = char
                    key_states[char] = True
            else:
                key_states[char] = False
        GPIO.output(line, GPIO.LOW)
        return pressed_key


    while True:
        stdscr.clear()
        stdscr.nodelay(True)
        text_ui.add_text(stdscr, align.center_vertical, f'{datetime.now().strftime("%Y-%m-%d    %H:%M")}', row=-12)
        if is_midnight(): 
            schedule = getschedule()
        try:
           if schedule:
               pass
        except:
           schedule = getschedule()
           text_ui.add_text(stdscr, align.center_vertical, f'updated!') 
        weekday = datetime.now().weekday()
        try:
            today_schedule = schedule[weekday+1]
        except:
            today_schedule = None
        row = 0
        if today_schedule:
            now_lesson = current_event(timetable)
            for i in range(len(today_schedule)):
                    try:
                        if now_lesson and now_lesson == i+1:
                            line = f"{i+1}  {timetable_print[i+1][0]} - {timetable_print[i+1][1]}       {today_schedule[str(i+1)][0]['subject_id']}"
                            text_ui.add_text(stdscr, align.left_vertical_scedule, line, row=row, color=curses.COLOR_WHITE, background=curses.COLOR_GREEN)
                            row += 1
                        else:
                            line = f"{i+1}  {timetable_print[i+1][0]} - {timetable_print[i+1][1]}       {today_schedule[str(i+1)][0]['subject_id']}"
                            text_ui.add_text(stdscr, align.left_vertical_scedule, line, row=row)
                            row += 1
                    except:
                        pass
        else:
            line = f"No lessons today"
            text_ui.add_text(stdscr, align.left_vertical_scedule, line, row=row)
        
        next_event_id, time_until_next_event = next_event(timetable)
        if next_event_id != "no_lessons":
            try:
                if next_event_id != 0:
                    line = f"next: {today_schedule[str(next_event_id)][0]['subject_id']} in {time_until_next_event}"
                    text_ui.add_text(stdscr, align.left_vertical_scedule, line, row=row+2)
                else:
                    line = f"next: break in {time_until_next_event}"
                    text_ui.add_text(stdscr, align.left_vertical_scedule, line, row=row+2)
            except:
                    text_ui.add_text(stdscr, align.left_vertical_scedule, "No more lessons today", row=row+2)
        else:
            text_ui.add_text(stdscr, align.left_vertical_scedule, time_until_next_event, row=row+2)

        if ping("192.168.0.188") == True:
            color1 = curses.COLOR_WHITE
            background1 = curses.COLOR_GREEN
        else:
            color1 = curses.COLOR_WHITE
            background1 = curses.COLOR_RED

        text_ui.add_text(stdscr, align.left_vertical, "Connection", row=10, color=color1, background=background1)

        line = f"* press q (S16) to exit"
        text_ui.add_text(stdscr, align.left_vertical, line, row=11)
        current_time = datetime.now().strftime("%H : %M")
        f = Figlet(font='basic')
        line ="\n"+f.renderText(current_time)

        text_ui.add_text(stdscr, align.left_vertical, line, row=1)
        stdscr.refresh()


        key = stdscr.getch()
        if key == ord('q'):
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

        time.sleep(0.1)



def main_forecast(stdscr):
    from screens.start_menu import main_screen

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
                    print(char)
                    pressed_key = char
                    key_states[char] = True
            else:
                key_states[char] = False
        GPIO.output(line, GPIO.LOW)
        return pressed_key

    api_key = '9f648ff524736faef82e196f838815aa'
    city = 'Odesa'
    while True:
        stdscr.clear()
        stdscr.nodelay(True)
        text_ui.add_text(stdscr, align.center_vertical, f'{datetime.now().strftime("%Y-%m-%d    %H:%M")}', row=-12)
    
        if is_midnight():
            forecast = get_weather_forecast(api_key, city)
        try:
           if forecast:
               pass
        except:
           forecast = get_weather_forecast(api_key, city)
           text_ui.add_text(stdscr, align.center_vertical, f'updated!') 

        forelist = forecast.split("\n")
        row = -10
        for i in forelist:
            text_ui.add_text(stdscr, align.left_vertical, i, row=row)
            row += 1

        

        if ping("192.168.0.188") == True:
            color1 = curses.COLOR_WHITE
            background1 = curses.COLOR_GREEN
        else:
            color1 = curses.COLOR_WHITE
            background1 = curses.COLOR_RED

        text_ui.add_text(stdscr, align.left_vertical, "Connection", row=10, color=color1, background=background1)

        line = f"* press q (S16) to exit"
        text_ui.add_text(stdscr, align.left_vertical, line, row=11)
        current_time = datetime.now().strftime("%H : %M")
        f = Figlet(font='basic')
        line ="\n"+f.renderText(current_time)

        text_ui.add_text(stdscr, align.left_vertical, line, row=1)
        stdscr.refresh()


        key = stdscr.getch()
        if key == ord('q'):
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

        time.sleep(0.1)