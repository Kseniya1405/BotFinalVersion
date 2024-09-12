from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создаём reply клавиатуру основного меню.
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Погода')],
    [KeyboardButton(text='Время'), KeyboardButton(text='Таймер')]
],
resize_keyboard=True, one_time_keyboard=True,
input_field_placeholder='Что сделать?')

# Создаём reply клавиатуру для меню выбора погоды.
weather = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='По городу'), KeyboardButton(text='По местоположению')]
],
resize_keyboard=True, one_time_keyboard=True,
input_field_placeholder='Что сделать?')

# Создаём reply клавиатуру для меню выбора времени.
time = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='По городу'), KeyboardButton(text='По местоположению')]
],
resize_keyboard=True, one_time_keyboard=True,
input_field_placeholder='Что сделать?')

# Создаём reply клавиатуру для передачи геопозиции.
geo = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Местоположение', request_location=True)]
],
resize_keyboard=True, one_time_keyboard=True,
input_field_placeholder='')

# Создаём reply клавиатуру для возвращения в главное меню.
menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Меню')]
],
resize_keyboard=True, one_time_keyboard=True,
input_field_placeholder='')
