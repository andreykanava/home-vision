import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def getschedule():
    subjects = {
        1: "Українська мова",
        62: "Хореографія",
        2: "Англійська мова",
        41: "Хімія",
        42: "Фізика",
        32: "Геометрія",
        31: "Алгебра",
        60: "Основи здоров'я",
        52: "Інформатика",
        51: "Трудове навчання",
        43: "Географія",
        40: "Біологія",
        10: "Історія України",
        5: "Зарубіжна література",
        4: "Українська література",
        88: "Мистецтво",
        57: "Фізкультура",
        11: "Всесвітня історія",
        30: "Математика",
        7586: "ІК «Пізнаємо природу»",
        27: "Муз. мист.",
        28: "Образотв мист",
        6: "Німецька мова",
        81: "Французька мова",
        22: "Громад освіта",
        13: "Правознавство",
        437: "Історія інтегр",
        6992: "Здоров’я, безпека та добробут",
        6991: "Вступ до історії України",
        54: "Технології"
    }
    url = "https://client.rozklad.org/files/rozklad/rr/r_1267.html"
    response = requests.get(url)
    response_text = response.text
    soup = BeautifulSoup(response_text, 'html.parser')

    # Ищем скрипт, содержащий нужные данные
    scripts = soup.find_all('script')
    for script in scripts:
        if 'var zaklad_id' in script.text:
            needed_script = script.text
            break

    # Находим и извлекаем JSON из скрипта
    start = needed_script.find('{')
    end = needed_script.rfind('}') + 1
    data_json = needed_script[start:end]
    data = json.loads(data_json)

    # Данные о расписании класса 10-МА
    class_10_ma = data['classes']['53272']['roz']

    # Структурируем данные в словарь
    schedule_dict = {}
    for day in range(1, 6):  # Предположим, что дни недели идут от 1 до 5
        day_schedule = class_10_ma.get(str(day), {})
        schedule_dict[day] = {}
        for lesson_number, lesson_details in day_schedule.items():
            schedule_dict[day][lesson_number] = [{
                'subject_id': subjects[detail['p']],
            } for detail in lesson_details]

    # Выводим расписание
    return schedule_dict

def current_event(timetable):
    now = datetime.now()

    for event_id, times in timetable.items():
        start_time = datetime.strptime(times[0], "%H:%M").time()
        end_time = datetime.strptime(times[1], "%H:%M").time()
        
        if start_time <= now.time() <= end_time:
            return event_id
    
    return False

def next_event(timetable):
    now = datetime.now()
    
    # Переменная для хранения наименьшего времени до начала следующего события
    min_delta = None
    next_event_id = None
    
    for event_id, times in timetable.items():
        start_time = datetime.strptime(times[0], "%H:%M").time()
        end_time = datetime.strptime(times[1], "%H:%M").time()
        
        # Время до начала события и до конца события
        start_delta = datetime.combine(datetime.now(), start_time) - now
        end_delta = datetime.combine(datetime.now(), end_time) - now
        
        # Если текущее время в диапазоне события, возвращаем 0 и время до конца события
        if start_time <= now.time() <= end_time:
            return 0, f"{((end_delta.seconds % 3600) // 60)+1}m"
        
        # Ищем следующее событие
        if start_delta.total_seconds() > 0:  # Если событие ещё не началось
            if min_delta is None or start_delta < min_delta:
                min_delta = start_delta
                next_event_id = event_id
    
    if next_event_id is not None:
        return next_event_id, f"{((min_delta.seconds % 3600) // 60)+1}m"
    
    # Если нет следующих событий сегодня
    return "no_lessons", "No more lessons today"

# Пример расписания
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

# Вызов функции
next_event_id, time_until_next_event = next_event(timetable)
print(next_event_id)
