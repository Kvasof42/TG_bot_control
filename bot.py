import os
import subprocess
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from dotenv import load_dotenv
from filters import IsAdmin

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def set_volume(level: int):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level / 100, None)
    
@dp.message(IsAdmin(), Command("vol_up"))
async def cmd_vol_up(message: types.Message):
    args = message.text.split()
    
    if len(args) < 2:
        await message.answer("Введите громкость после команды, например: /vol_up 50")
        return

    try:
        value = int(args[1])
    except ValueError:
        await message.answer("Ошибка: введите число от 0 до 100")
        return

    if not (0 <= value <= 100):
        await message.answer("Ошибка: число должно быть от 0 до 100")
        return
    

    set_volume(value)
    await message.answer(f"Громкость установлена на {value}%")

@dp.message(IsAdmin(), Command("shutdown"))
async def cmd_shutdown(message: types.Message):
    await message.answer("Выключаю компьютер...")
    subprocess.run("shutdown /s /t 1", shell=True)

@dp.message(IsAdmin(), Command("sleep"))
async def cmd_sleep(message: types.Message):
    await message.answer("Перевожу в спящий режим...")
    subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)

@dp.message(IsAdmin(), F.document)
async def handle_docs(message: types.Message):
    file = await bot.get_file(message.document.file_id)
    await bot.download_file(file.file_path, f"downloads/{message.document.file_name}")
    await message.answer(f"Файл {message.document.file_name} сохранен!")

if __name__ == "__main__":
    dp.run_polling(bot)