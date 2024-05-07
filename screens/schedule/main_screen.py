import curses
from utils import align, menu_track
from components.menu import menu_ui
from components.text import text_ui
from screens.schedule.schedule_utlis import getschedule, current_event, next_event
from datetime import datetime
import time

def is_midnight():
    # Получаем текущее время
    current_time = datetime.now()
    
    # Проверяем, что часы и минуты равны 00:00
    if current_time.hour == 0 and current_time.minute == 0:
        return True
    else:
        return False

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
        print(next_event_id)
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

        line = f"* press q to exit"
        text_ui.add_text(stdscr, align.left_vertical, line, row=11)
        line = """
         ,MMM8&&&.
    _...MMMMM88&&&&..._
 .::'''MMMMM88&&&&&&'''::.
::     MMMMM88&&&&&&     ::
'::....MMMMM88&&&&&&....::'
   `''''MMMMM88&&&&''''`
         'MMM8&&&'
        """
        text_ui.add_text(stdscr, align.left_vertical, line, row=1)
        stdscr.refresh()
        time.sleep(30)


        key = stdscr.getch()
        if key == ord('q'):
            curses.wrapper(main_screen)
