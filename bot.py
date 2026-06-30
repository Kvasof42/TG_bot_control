import asyncio
import os
import subprocess
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from dotenv import load_dotenv
from filter import IsAdmin


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'), IsAdmin())
async def start(message: types.Message):
    first_name = message.from_user.first_name
    await message.answer(f'Привет! {first_name}. Этот бот для контроля ПК')
    
def set_volume(level):
    devices = AudioUtilities.GetSpeakers()

    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )

    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level / 100.0, None)
    
@dp.message(Command("vol_up"), IsAdmin())
async def cmd_vol_up(message: types.Message):
    try:
        value = int(message.text.split(maxsplit=1)[1])

        if not 0 <= value <= 100:
            raise ValueError

        set_volume(value)
        await message.answer(f"Громкость установлена на {value}%")

    except IndexError:
        await message.answer("Использование:\n/vol_up 50")

    except ValueError:
        await message.answer("Введите число от 0 до 100")

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
    os.makedirs("downloads", exist_ok=True)
    file = await bot.get_file(message.document.file_id)
    await bot.download_file(file.file_path, f"downloads/{message.document.file_name}")
    await message.answer(f"Файл {message.document.file_name} успешно сохранен!")
    

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())