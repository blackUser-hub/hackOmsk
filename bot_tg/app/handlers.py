from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.keyboards import *
import app.requests as rq
router = Router()

class userReg(StatesGroup):
    fio = State()
    type_of_employee = State()



@router.message(StateFilter(None), CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(userReg.fio)
    await message.answer(text="Добро пожаловать в ИИ-секретаря от Правительства РФ! \nДля продолжения введите ваши ФИО:")

@router.message(userReg.fio)
async def fio_setting(message: Message, state: FSMContext):
    if isinstance(message.text, str) and len(message.text.split(sep=" ")) == 3:
        await state.update_data(fio=message.text)
        data = await state.get_data()
        # await rq.init_user(message.from_user.id, data["fio"], message.from_user.username)
        await message.answer(text="Отлично, регистрация прошла успешно, нажмите кнопку ниже, чтобы перейти в профиль", reply_markup=reg_kb(message.from_user.id))
        await state.clear()
    else:
        await message.answer(text="Вы ввели некорректные ФИО")


@router.callback_query(F.data.startswith("profile"))
async def profile_callback(call: CallbackQuery, state: FSMContext):
    # user_data = await rq.get_user(call.data.split(sep=" ")[1])
    user_data = {"name": "Синица Александр Павлович"}
    await call.message.answer(text=f"Добро пожаловать, {user_data['name']}!\nЧто вы хотите сделать?")

    
    
    
