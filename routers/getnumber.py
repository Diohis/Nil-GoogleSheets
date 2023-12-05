import logging
import os
import gspread
from aiogram import Bot, Dispatcher, Router, types,F
from aiogram.filters import CommandStart, CommandObject, BaseFilter
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials\

load_dotenv()
scope = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file('cred.json')
client = gspread.authorize(credentials.with_scopes(scope))
sheet = client.open_by_url(os.getenv("SHEET_URL"))

router = Router()


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Поделиться контактом", request_contact=True))
    await message.answer(
        f"Приветствую {message.from_user.username} в боте сборщика информации",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    
@router.message((F.contact!=None and F.contact.user_id == F.from_user.id))
async def menu1(message: types.Message):
    worksheet = sheet.get_worksheet(6)
    if worksheet.find(f"{message.from_user.id}")==[]:
        await message.reply("Вы уже поделились контактом ранее!")
        return
    column_index = 1  # Индекс столбца, в котором нужно записать данные (начиная с 1)
    # Получение последней заполненной ячейки в столбце
    row_index = len(worksheet.get_all_values())+1

    worksheet.update_cell(row_index, column_index, message.contact.user_id)
    worksheet.update_cell(row_index, column_index+1, message.contact.first_name)
    worksheet.update_cell(row_index, column_index+2, message.contact.phone_number)
    await message.reply("Спасибо за информацию!")