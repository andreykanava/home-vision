import asyncio
import subprocess
import telebot

TOKEN = ""
CHAT_ID =
def telegram_send_message(message):
    bot = telebot.TeleBot(TOKEN)
    bot.send_message(CHAT_ID, message)
async def check_connection():
    counter = 0
    while True:
        try:
            # Пингуем компьютер
            process = await asyncio.create_subprocess_exec(
                "ping", "-c", "1", "computer_ip_address",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode == 0:
                pass
            else:
                counter = counter + 1
                telegram_send_message(counter)
                if counter >= 10:
                    telegram_send_message("Отлючение от сети, подключение блокируеться.")
                    subprocess.run(["sudo", "systemctl", "start", "parprouted"])
                    counter = 0
                    break
        except Exception as e:
            telegram_send_message("Error while checking connection. ", e)
        await asyncio.sleep(1)