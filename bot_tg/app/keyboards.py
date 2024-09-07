from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def reg_kb(tg_id) -> InlineKeyboardMarkup:
    but = InlineKeyboardButton(text="Перейти в профиль 🙎‍♂️", callback_data=f"profile {tg_id}")
    return InlineKeyboardMarkup(inline_keyboard=[[but]])

def profile_kb() -> InlineKeyboardMarkup:
    but = InlineKeyboardButton(text="Загрузить запись переговоров✅", callback_data="download")
    return InlineKeyboardMarkup(inline_keyboard=[[but]])