from aiogram import  F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType
from aiogram.fsm.state import State, StatesGroup
from app.keyboards import *
import app.requests as rq
import logging
from app.bot_instance import bot, dp
import os
import aiohttp
import asyncio



from config import backend_api_url

logger = logging.getLogger(__name__)


router = Router()

class userReg(StatesGroup):
    password = State()
    sending_file = State()




@router.message(StateFilter(None), CommandStart())
async def start(message: Message, state: FSMContext):
    if (await rq.get_user(int(message.from_user.id))) == {}:

        await state.set_state(userReg.password)
        await message.answer(text="Добро пожаловать в ИИ-секретаря от Правительства РФ! \nДля продолжения придумайте пароль для разблокировки скачивания файлов (Латинские буквы и цифры):")
    else:
        await message.answer(text="Вы уже зарегистрированы", reply_markup=reg_kb(int(message.from_user.id)))

@router.message(userReg.password)
async def fio_setting(message: Message, state: FSMContext):
    if isinstance(message.text, str) and len(message.text.split(sep=" ")) == 1:
        await state.update_data(password=message.text)
        data = await state.get_data()
       
        await rq.init_user(message.from_user.id, message.from_user.username,  str(data["password"]), 0, 0)
        user_id = message.from_user.id
        await message.delete()
        await message.answer(text="Отлично, регистрация прошла успешно, нажмите кнопку ниже, чтобы перейти в профиль", reply_markup=reg_kb(message.from_user.id))
        await state.clear()
    else:
        await message.answer(text="Вы ввели некорректный тип пароля")


@router.callback_query(F.data.startswith("profile"))
async def profile_callback(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    user_data = await rq.get_user(int(call.data.split(sep=" ")[1]))
    # user_data = {"name": "Синица Александр Павлович"}
    await call.message.answer(text=f"Добро пожаловать, {user_data['username']}!\nЧто вы хотите сделать?", reply_markup=profile_kb())

@router.callback_query(F.data.startswith("download"))
async def download_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(userReg.sending_file)
    user_data = await rq.get_user(int(call.from_user.id))
    await call.message.answer("Загрузите файл ваших переговоров")

@router.callback_query(F.data.startswith("otchets"))
async def otchets_callback(call: CallbackQuery):
    sd = await rq.get_otchets(call.from_user.id)
    await call.message.answer("Выберете интересующие вас отчеты совещания", reply_markup=otchet_kb(sd))

@router.callback_query(F.data.startswith("idotchet_"))
async def idotchet_callback(call: CallbackQuery):
    otchet_id = int(call.data.replace("idotchet_", ""))
    otchet = await rq.get_otchet_from_id(otchet_id)
    await call.message.answer(f"{otchet[3]}")


AUDIO_DIR = os.path.join('app', 'audio_files')
os.makedirs(AUDIO_DIR, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    # Remove any invalid characters from the filename
    return ''.join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

@router.message(userReg.sending_file)
async def handle_audio(message: types.Message, state: FSMContext):
    audio = message.audio
    file_info = await bot.get_file(audio.file_id)
    file_path = file_info.file_path
    sanitized_filename = sanitize_filename(audio.file_name)
    destination = os.path.join(AUDIO_DIR, sanitized_filename)
    
    async def download_with_retry(file_path, destination, retries=3):
        for attempt in range(retries):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=300)) as session:  # Increased timeout
                    await bot.download_file(file_path, destination)
                await message.reply(f"Аудиофайл {sanitized_filename} успешно загружен и сохранен!")
                await rq.add_task(message.chat.id, f"app/audio_files/{sanitized_filename}")
                return
            except asyncio.TimeoutError:
                if attempt < retries - 1:
                    await message.reply(f"Попытка {attempt + 1} не удалась, повторная загрузка...")
                    await asyncio.sleep(2)  # Delay between retries
                else:
                    await message.reply("Ошибка: Превышено время ожидания при загрузке аудиофайла.")
                    break
            except Exception as e:
                await message.reply(f"Ошибка: {str(e)}")
                break
    
    # Attempt to download the file with retries
    await download_with_retry(file_path, destination)