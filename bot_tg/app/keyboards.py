from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def reg_kb(tg_id) -> InlineKeyboardMarkup:
    but = InlineKeyboardButton(text="Перейти в профиль 🙎‍♂️", callback_data=f"profile {tg_id}")
    return InlineKeyboardMarkup(inline_keyboard=[[but]])

def profile_kb() -> InlineKeyboardMarkup:
    but = InlineKeyboardButton(text="Загрузить запись переговоров✅", callback_data="download")
    but2 = InlineKeyboardButton(text="Посмотреть отчеты📊", callback_data="otchets")
    return InlineKeyboardMarkup(inline_keyboard=[[but, but2]])


def otchet_kb(user_otchets) -> InlineKeyboardMarkup:
    buttons = []
    for i in range(len(user_otchets)):
        buttons.append([InlineKeyboardButton(text=str(user_otchets[i]['id']), callback_data=f"idotchet_{user_otchets[i]['id']}")])
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup
