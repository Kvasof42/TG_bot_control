import asyncio
import os
import subprocess
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv
from filter import IsAdmin
from service.volume import router as volume_router
from handlers.downloads import router as downloads_router
from aiogram.types import BotCommand

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(volume_router)
dp.include_router(downloads_router)

@dp.message(Command('start'), IsAdmin())
async def start(message: types.Message):
    first_name = message.from_user.first_name
    await message.answer(f'Привет! {first_name}. Этот бот для контроля ПК')
    
@dp.message(Command('help'), IsAdmin())
async def help(message: types.Message):
    await message.answer(
        'Телеграмм бот для контроля ПК',
        'Все комманды в menu'
        'Если отправить фото/видео/документ сохраниться в папку файл'
    )

@dp.message(IsAdmin(), Command("shutdown"))
async def cmd_shutdown(message: types.Message):
    await message.answer("Выключаю компьютер...")
    subprocess.run("shutdown /s /t 1", shell=True)

@dp.message(IsAdmin(), Command("sleep"))
async def cmd_sleep(message: types.Message):
    await message.answer("Перевожу в спящий режим...")
    subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)

    
async def main():
    await dp.start_polling(bot)
    
    await bot.set_my_commands([
        BotCommand(command="start", description="В начало"),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='shutdown', description='Выключить компьютер'),
        BotCommand(command="sleep", description="Спящий режим"),
        BotCommand(command="vol_up", description="Установить громкость")
    ])

if __name__ == "__main__":
    asyncio.run(main())