from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Погода')],
    [KeyboardButton(text='Время'), KeyboardButton(text='Таймер')]
],
resize_keyboard=True,
input_field_placeholder='Что сделать?')


weather = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='По городу'), KeyboardButton(text='По местоположению')]
],
resize_keyboard=True,
input_field_placeholder='Что сделать?')

time = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='По городу'), KeyboardButton(text='По местоположению')]
],
resize_keyboard=True,
input_field_placeholder='Что сделать?')

geo = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Местоположение', request_location=True)]
],
resize_keyboard=True,
input_field_placeholder='')