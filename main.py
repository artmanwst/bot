from aiogram import (
    Bot,
    Dispatcher,
    types
)
from aiogram.types.web_app_info import WebAppInfo
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F
import os
import asyncio
import sqlite3


bot = Bot(token='6662652848:AAG_sTyrZTx-vz2lC9bIhs5TvTZd1Ora9hY')
db = Dispatcher()


class Registration(StatesGroup):
    check_user = State()
    name = State()
    age = State()
    count = State()


@db.message(Command("start"))
async def keyboard(message: types.Message):
    url = 'https://127.0.0.1:9000'
    text = 'Посчитать кол-во пользователей'
    text2 = 'Зарегистрироваться'
    kb = [
        [types.KeyboardButton(text=text, web_app=WebAppInfo(url=url)),
         types.KeyboardButton(text=text2)],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text='Добрый день!', reply_markup=keyboard)


@db.message(F.text == 'Зарегистрироваться')
async def check_user(message: types.Message, state: FSMContext):
    database_path = os.path.join('webapp', 'db.sqlite3')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    user_id = message.from_user.id
    id = cursor.execute('''SELECT *  from counter_user WHERE id =?''',
                        (user_id,))
    id = id.fetchone()
    if id is None:
        text = 'Пожалуйста, введите свое имя'
        await message.answer(text)
        await state.set_state(Registration.name)
    else:
        text = 'Вы уже зарегистрированы'
        print('a')
        await message.answer(text)



@db.message(StateFilter(Registration.name))
async def name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    text = 'Теперь введите свой возраст'
    await message.answer(text)
    await state.set_state(Registration.age)



@db.message(StateFilter(Registration.age))
async def age_user(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        data = await state.get_data()
        database_path = os.path.join('webapp', 'db.sqlite3')
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        id = message.from_user.id
        name = data['name']
        age = data['age']
        cursor.execute('''INSERT INTO counter_user (id,name,age)
                         VALUES(?,?,?)''', (id, name, age))
        conn.commit()
        conn.close()
        await message.answer("Спасибо, вы зарегистрированы!")
    except ValueError:
        await message.answer("Неверный формат. Введите возраст цифрами.")
        return


async def main():
    await db.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
