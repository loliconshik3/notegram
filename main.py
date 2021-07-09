from aiogram import Bot, Dispatcher, executor, types, md
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import logging
import database
import random
import config
import requests

API_TOKEN = config.TOKEN
db = database.Database()
db.Init()

#Configure logging 
logging.basicConfig(level=logging.INFO)

#Init bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user = message.from_user
    db.UserInit(user)

    note_kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(KeyboardButton("[Добавить заметку]"))
    
    await message.reply("Привет! Пока что у тебя нет заметок, так что нажми на кнопку, чтобы они появились!", reply_markup=note_kb)

@dp.message_handler()
async def get_all_messages(message: types.Message):
    user = message.from_user
    last_input = db.get("users", "last_input", user.id)
    user_notes = eval(db.get("users", "notes", user.id))
    user_input_status = eval(db.get("users", "input_status", user.id))
    note_kb    = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    if not user_input_status["name_input"] and not user_input_status["description_input"]:
        if message.text == "[Добавить заметку]":
            user_input_status["name_input"] = True
            db.set("users", "input_status", user.id, str(user_input_status))
            await message.reply("Напиши имя для твоей заметки.")
            return

        if user_notes != {}:
            
            for note in user_notes.keys():
                if note not in message.text:
                    note_kb.add(KeyboardButton(f"{note} | {user_notes[note]['date']}"))
                else:
                    await message.reply(user_notes[note]["description"])
                    return
            note_kb.add(KeyboardButton("[Добавить заметку]"))
                    
            await message.reply(f'Это все твои заметки. Выбирай.', reply_markup = note_kb)

        else:
            note_kb.add(KeyboardButton("[Добавить заметку]"))
        
            await message.reply(f"У тебя нет никаких заметок...", reply_markup = note_kb)
    else:
        if user_input_status["description_input"]:
            user_notes[last_input] = {"description" : message.text, "date": str(message.date)}
            db.set('users', 'notes', user.id, str(user_notes))
            user_input_status = {"name_input": False, "description_input": False}
            db.set('users', 'input_status', user.id, str(user_input_status))

            for note in user_notes.keys():
                note_kb.add(KeyboardButton(f"{note} | {user_notes[note]['date']}"))

            note_kb.add(KeyboardButton("[Добавить заметку]"))

            await message.reply(f"Заметка сохранена!", reply_markup = note_kb)
            return
    
        if user_input_status["name_input"]:
            db.set('users', 'last_input', user.id, message.text)
            user_input_status["description_input"] = True
            db.set('users', 'input_status', user.id, str(user_input_status))
            await message.reply(f"Каркас заметки создан, теперь настало время написать саму заметку.")
            return
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
