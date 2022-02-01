from aiogram.types.message import ContentType
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

#Inline KeyBoard

reg_success = InlineKeyboardButton("Согласится",callback_data="reg_success")
reg_markup = InlineKeyboardMarkup().add(reg_success)

info_full = InlineKeyboardButton("💲Купить полный доступ💲", callback_data="info_full")
info_markup = InlineKeyboardMarkup().add(info_full)

pay_full_yoo = InlineKeyboardButton("ЮКасса", callback_data="yookassa")
pay_full_sber = InlineKeyboardButton("СберБанк", callback_data="sberbank")
pay_full = InlineKeyboardMarkup().add(pay_full_yoo, pay_full_sber)