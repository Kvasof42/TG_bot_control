import os
from PIL import ImageGrab
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from filter import IsAdmin

router = Router()

@router.message(Command("screen"), IsAdmin())
async def cmd_screen(message: types.Message):
    screenshot = ImageGrab.grab()
    file_path = "temp_screen.png"
    screenshot.save(file_path)
    
    photo = FSInputFile(file_path)
    await message.answer_photo(photo=photo, caption="Скриншот экрана")
    
    os.remove(file_path)