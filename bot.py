import asyncio, os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Text

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("Set TOKEN env-var!")

bot = Bot(TOKEN, parse_mode="HTML")
dp  = Dispatcher()

@dp.message(CommandStart())
async def start(m: types.Message):
    await m.answer("👋 Привет! Railway + aiogram 3. Напиши ping.")

@dp.message(Text("ping"))
async def ping(m: types.Message):
    await m.answer("pong")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        "🥃 Виски", "🧊 Водка", "🍺 Пиво",
        "🍷 Вино", "📋 Тесты", "🍹 Коктейли", "🦌 Ягермейстер"
    )
    await message.answer("Привет! Выбери категорию:", reply_markup=kb)

@dp.message_handler(Text(equals="Назад"))
async def go_back(message: types.Message):
    await send_welcome(message)


async def 
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
