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

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
