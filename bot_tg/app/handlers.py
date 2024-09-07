from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType
from aiogram.fsm.state import State, StatesGroup
from app.keyboards import *
import app.requests as rq
import logging


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
        await rq.init_user(message.from_user.id, message.from_user.username,  data["password"], 0, 0)
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


    
