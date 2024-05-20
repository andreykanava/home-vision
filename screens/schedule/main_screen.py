import curses
from utils import align, menu_track
from components.menu import menu_ui
from components.text import text_ui
from screens.schedule.schedule_utlis import getschedule, current_event, next_event
from datetime import datetime
import time
import asyncio
import subprocess

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

def main_schedule(stdscr):
    from screens.start_menu import main_screen
    from screens.NetworkManager.main_screen import main_network

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

        line = f"* press q to exit   ||   press n to enter network manager"
        text_ui.add_text(stdscr, align.left_vertical, line, row=11)
        line = """
 _______  _______  ______    ___     
|       ||       ||    _ |  |   |    
|  _____||   _   ||   | ||  |   |    
| |_____ |  | |  ||   |_||_ |   |    
|_____  ||  |_|  ||    __  ||   |___ 
 _____| ||      | |   |  | ||       |
|_______||____||_||___|  |_||_______|
"""
        text_ui.add_text(stdscr, align.left_vertical, line, row=1)
        stdscr.refresh()
        time.sleep(3)


        key = stdscr.getch()
        if key == ord('q'):
            curses.wrapper(main_screen)
        if key == ord('n'):
            curses.wrapper(main_network)
