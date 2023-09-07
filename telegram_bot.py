from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram import Bot, types
import logging
import sqlite3
import requests
import json
 


BOT_TOKEN = '1367782105:AAEjam0Wdz3Dbff897lQTlxfjKT0Pmc9aD8'  

storage = MemoryStorage()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()


@dp.message_handler(commands=['start', 'menu'])
async def start_menu(message: types.Message):
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Отправьте мне ваш токен полученный из вашего профиля на сайте http://127.0.0.1:8000/'
            )


async def get_token_from_txt(user_id: int):
    with open('user_tokens.txt', 'r') as f:
        for lines in f.readlines(): 
            if lines.find(str(user_id)) >= 0:
                return lines.strip().split(':')[1]
        f.close()
        

@dp.message_handler(content_types=['text'])
async def message_user(message: types.Message):
    if message.text.find('sha256') >= 0:
        token = await get_token_from_txt(message.from_user.id)
        if token:
            await bot.send_message(message.from_user.id, 'Вы уже отправляли токен!')
        else:
            await bot.send_message(message.from_user.id, 'Ваш токен принят и сохранен!')
            with open('user_tokens.txt', 'a') as f:
                f.write(f'{message.from_user.id}:{message.text}\n')
                f.close()
    else:
        token = await get_token_from_txt(message.from_user.id)
        users = json.loads(requests.get(url='http://127.0.0.1:8000/users/').text)     
        for user in users:   
            if token == user['password']:
                first_name = user['first_name']
                break
            else: first_name = ''

        if first_name:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f'{first_name}, я получил от тебя сообщение:\n{message.text}'
            )
            r = requests.post(
                url='http://127.0.0.1:8000/post/', 
                data={'token': user['password'], 'text': message.text}
            )
        else:
            await bot.send_message(
                chat_id=message.from_user.id,
                text='Отправьте мне ваш токен полученный из вашего профиля на сайте '
            )



if __name__ == '__main__':
    executor.start_polling(dp)






