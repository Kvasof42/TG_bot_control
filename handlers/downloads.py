import os
from aiogram import Bot
from aiogram import Router, types, F
from filter import IsAdmin

router = Router()

FORBIDDEN_EXTENSIONS = ('.exe', '.bat', '.sh', '.py', '.msi', '.cmd')

def ensure_folder(path: str):
    os.makedirs(path, exist_ok=True)

def is_safe_filename(filename: str) -> bool:
    if not filename:
        return False
    clean_name = os.path.basename(filename)
    if clean_name.lower().endswith(FORBIDDEN_EXTENSIONS):
        return False
    return True

@router.message(IsAdmin(), F.document)
async def handle_docs(message: types.Message, bot: Bot):
    file_name = message.document.file_name
    
    if not is_safe_filename(file_name):
        await message.answer("Ошибка: Файл имеет недопустимый формат или имя.")
        return

    ensure_folder("downloads/documents")
    file = await bot.get_file(message.document.file_id)
    destination = os.path.join("downloads/documents", os.path.basename(file_name))
    await bot.download_file(file.file_path, destination)
    await message.answer(f"Файл {os.path.basename(file_name)} успешно сохранен!")

@router.message(IsAdmin(), F.photo)
async def handle_photo(message: types.Message, bot: Bot):
    ensure_folder("downloads/photos")
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    await bot.download_file(
        file.file_path,
        destination=f"downloads/photos/{photo.file_unique_id}.jpg"
    )
    await message.answer("Фото сохранено!")

@router.message(IsAdmin(), F.video)
async def handle_video(message: types.Message, bot: Bot):
    file_name = message.video.file_name
    if file_name and not is_safe_filename(file_name):
        await message.answer("Ошибка: Видеофайл имеет недопустимое имя.")
        return

    ensure_folder("downloads/videos")
    file = await bot.get_file(message.video.file_id)
    
    safe_name = os.path.basename(file_name) if file_name else f"{message.video.file_unique_id}.mp4"
    await bot.download_file(file.file_path, destination=f"downloads/videos/{safe_name}")
    await message.answer("Видео сохранено!")