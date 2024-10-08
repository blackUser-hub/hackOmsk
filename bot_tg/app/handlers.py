from aiogram import  F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_file import FSInputFile
from app.keyboards import *
import app.requests as rq
import logging
from app.bot_instance import bot, dp
import os
import aiohttp
import asyncio
import ml
import config
from pathlib import Path
from processing import docx2pdf, createpass


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

@router.callback_query(F.data.startswith("transcript_download_"))
async def senddec_callback(call: CallbackQuery):
    otchet_id = int(call.data.replace("transcript_download_", ""))
    otchet = await rq.get_otchet_from_id(otchet_id)
    document = FSInputFile(otchet[7])
    await bot.send_document(call.from_user.id, document)
@router.callback_query(F.data.startswith("protocol_download_"))
async def protocol_download_callback(call: CallbackQuery):
    otchet_id = int(call.data.replace("protocol_download_", ""))
    otchet = await rq.get_otchet_from_id(otchet_id)
    document = FSInputFile(otchet[5])
    await bot.send_document(call.from_user.id, document)
@router.callback_query(F.data.startswith("protocol_download_pdf_"))
async def protocol_download_pdf_(call: CallbackQuery):
    otchet_id = int(call.data.replace("protocol_download_pdf_", ""))
    otchet = await rq.get_otchet_from_id(otchet_id)
    document = FSInputFile(otchet[6])
    await bot.send_document(call.from_user.id, document)

@router.callback_query(F.data.startswith("idotchet_"))
async def idotchet_callback(call: CallbackQuery):
    otchet_id = int(call.data.replace("idotchet_", ""))
    otchet = await rq.get_otchet_from_id(otchet_id)
    otchet_status = otchet[8]
    if otchet_status == 1:
        await call.message.answer(f"Аудио обрабатывается... ")
    elif otchet_status == 2:
        
        await call.message.answer(f"{otchet[2]}", reply_markup=otchet_about_kb(otchet_id))
    


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
    user = rq.get_user(message.from_user.id)
    
    async def download_with_retry(file_path, destination, retries=3):
        for attempt in range(retries):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=300)) as session:  # Increased timeout
                    await bot.download_file(file_path, destination)
                await message.reply(f"Аудиофайл {sanitized_filename} успешно загружен и сохранен!")
                await rq.add_task(message.chat.id, f"app/audio_files/{sanitized_filename}")
                await ml.diarize_transcript_audio(f"app/audio_files/{sanitized_filename}", message.chat.id)
                
                audio_path = f"app/audio_files/{sanitized_filename}"
                filename = Path(audio_path).stem
                await ml.create_descrypt_file(audio_path=audio_path)
                text = await ml.get_text(f"app/audio_files/{sanitized_filename}")
                yandexgpttext = await ml.yandexgpt(text,prompt=config.prompt)
                await ml.create_doc_from_text(yandexgpttext, audio_path)
                otch_id = await rq.get_last_task_id(message.chat.id)
                docx2pdf(f"app/outputs/{filename}/docx.docx", f"app/outputs/{filename}/pdf.pdf")
                createpass(f"app/outputs/{filename}/pdf.pdf", user["password"])
                createpass(f"app/outputs/{filename}/docx.docx", user["password"])
                await rq.add_all_to_task(id=otch_id,yandexgpt_text=yandexgpttext,output_csv_path=f"app/outputs/{filename}/transcription.csv",otchet_docx_path=f"app/outputs/{filename}/docx.docx",otchet_pdf_path=f"app/outputs/{filename}/pdf.pdf",transcript_docx_path=f"app/outputs/{filename}/decryption.docx",status=2)
                # добавить функцию док -- пдф
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