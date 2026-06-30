import os
from aiogram import Bot
from aiogram import Router, types, F
from filter import IsAdmin

router = Router()

def ensure_folder(path: str):
    os.makedirs(path, exist_ok=True)
    

@router.message(IsAdmin(), F.document)
async def handle_docs(message: types.Message, bot: Bot):
    ensure_folder("downloads/documents")
    file = await bot.get_file(message.document.file_id)
    await bot.download_file(file.file_path, f"downloads/documents/{message.document.file_name}")
    await message.answer(f"Файл {message.document.file_name} успешно сохранен!")


@router.message(IsAdmin(), F.photo)
async def handle_photo(message: types.Message, bot: Bot):
    ensure_folder("downloads/photos")
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    await bot.download_file(
        file.file_path,
        destination=f"downloads/photos/{photo.file_unique_id}.jpg"
    )
    await message.answer(f"Фото {photo.file_unique_id} сохранено!")
    

@router.message(IsAdmin(), F.video)
async def handle_video(message: types.Message, bot: Bot):
    ensure_folder("downloads/videos")
    file = await bot.get_file(message.video.file_id)
    await bot.download_file(
        file.file_path,
        destination=f"downloads/videos/{message.video.file_name or message.video.file_unique_id}.mp4"
    )
    await message.answer("Видео сохранено!")