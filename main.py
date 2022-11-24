from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from parser import login
from config import TOKEN
from db import Db

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    db = Db()
    if db.check_user(chat_id):
        await message.answer(
            f'''<strong>Assalomu aleykum {first_name} 👋</strong>\n@school_scores_bot botiga hush kelibsiz!''')
    else:
        await message.answer("Kundalik platformadagi login va parolingizni kiriting (login - parol)")
    db.close()


@dp.message_handler(content_types=['text'], regexp=r'\w+ - +\w+')
async def get_command_search(message: types.Message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    login, password = message.text.split(' - ')

    db = Db()
    if db.check_user(chat_id):
        db = Db()
        db.update_user(chat_id, login, password)
        await message.answer(
            f'''Ma'lumotlar yangilandi!''')
    else:
        db.add_user(chat_id, first_name, last_name, username, login, password)
        await message.answer(
            f'''<strong>Assalomu aleykum {first_name} 👋</strong>\n@school_scores_bot botiga hush kelibsiz!''')
    db.close()


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Bu bot orqali jonli ravishda bugungi maktab jadvalini kuzatib borishingiz mumkin!\nKundalik platformasi malumotlarinin yangilash uchun\n(login - parol) jo'nating")


from datetime import datetime


@dp.message_handler(commands=['schedule'])
async def process_help_command(message: types.Message):
    chat_id = message.chat.id
    db = Db()
    login_str, password = db.get_user(chat_id)
    subjects = login(login_str, password)['schedule']
    final_message = []
    i = 0
    for subject in subjects:
        i += 1
        final_message.append(
            f'{i}) <strong>{subject["subject"]["name"]}</strong> - <code>{subject["theme"]}</code> <i>({subject["hours"]["startHour"]}:{subject["hours"]["startMinute"]}-{subject["hours"]["endHour"]}:{subject["hours"]["endMinute"]})</i>')
    await message.answer("\n".join(final_message))


@dp.message_handler(commands=['marks'])
async def process_help_command(message: types.Message):
    chat_id = message.chat.id
    db = Db()
    login_str, password = db.get_user(chat_id)
    subjects = login(login_str, password)['marks']
    final_message = []
    for subject in subjects:
        date = datetime.utcfromtimestamp(int(subject["date"])).strftime("%Y-%m-%d")
        date_hours = datetime.utcfromtimestamp(int(subject["date"])).strftime("%H:%M:%S")
        final_message.append(
            f'<strong>{subject["subject"]["name"]} - {subject["marks"][0]["value"]}</strong> <i>({subject["markTypeText"]}, {date})</i>')
    await message.answer("\n".join(final_message))


# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)
