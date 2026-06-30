from aiogram import Router, types, F
from aiogram.filters import Command
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from filters import IsAdmin

router = Router()

def set_volume(level):
    devices = AudioUtilities.GetSpeakers()

    interface = devices.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )

    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level / 100.0, None)
    
@router.message(Command("vol_up"), IsAdmin())
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
