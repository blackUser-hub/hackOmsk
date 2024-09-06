from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def reg_kb(tg_id) -> InlineKeyboardMarkup:
    but = InlineKeyboardButton(text="Перейти в профиль 🙎‍♂️", callback_data=f"profile {tg_id}")
    return InlineKeyboardMarkup(inline_keyboard=[[but]])