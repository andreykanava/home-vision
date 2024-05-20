import asyncio
import subprocess
import telebot
import time

TOKEN = "7152868520:AAElEvnIFNhZbtrjQCVfdzThsSh8HUg5qSo"
CHAT_ID = 684248883
def telegram_send_message(message):
    bot = telebot.TeleBot(TOKEN)
    bot.send_message(CHAT_ID, message)

def check_connection():
    counter = 0
    while True:
        try:
            # Выполняем команду ping
            process = subprocess.run(
                ["ping", "-c", "1", "192.168.0.188"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if process.returncode == 0:
                pass
            else:
                #telegram_send_message(f"{counter}")
                counter += 1
                if counter >= 5:
                    telegram_send_message("Не удалось подключиться 5 раз подряд, отключение от службы.")
                    subprocess.run(["sudo", "systemctl", "stop", "parprouted"])
                    counter = 0
                    break
        except Exception as e:
            telegram_send_message(f"Error while checking connection: {e}")
        time.sleep(1)
