from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
def user_keyboard():
    buttons = [
        [KeyboardButton(text="Далее")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )