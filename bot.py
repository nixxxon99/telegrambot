import os
import asyncio
import logging
import random

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, Text
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)

# ---------------------------------------------------------------------------
# Конфигурация и инициализация
# ---------------------------------------------------------------------------
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("Set TOKEN env-var!")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()
router = Router()
dp.include_router(router)

# ---------------------------------------------------------------------------
# Словари с описаниями и фотографиями
# ---------------------------------------------------------------------------

def kb_row(*buttons: str) -> list[list[KeyboardButton]]:
    """Быстрое создание клавиатуры с одной строкой."""
    return [[KeyboardButton(text=b) for b in buttons]]

CATEGORY_KB = ReplyKeyboardMarkup(
    keyboard=[
        *kb_row("🥃 Виски", "🧊 Водка", "🍺 Пиво"),
        *kb_row("🍷 Вино", "📋 Тесты", "🍹 Коктейли"),
        *kb_row("🦌 Ягермейстер"),
    ],
    resize_keyboard=True,
)

# ------------------------------  Виски  ------------------------------------
WHISKY_DATA = {
    "Monkey Shoulder": {
        "photo": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Monkey_Shoulder_scotch_bottle.jpg",
        "text": (
            "1. Monkey Shoulder — это купажированный шотландский виски, созданный винокурней William Grant & Sons.\n"
            "2. Он сочетает солода Glenfiddich, Balvenie и Kininvie, придавая напитку глубокий и многослойный характер.\n"
            "3. В аромате отчётливо слышны ноты ванили, мёда и лёгкой цитрусовой свежести.\n"
            "4. Во вкусе проявляются карамель, тёплые специи и тонкий оттенок тостового хлеба.\n"
            "5. Крепость виски составляет 40%, что делает его универсальным как для чистого употребления, так и для коктейлей.\n"
            "6. Тёплая, обволакивающая текстура позволяет наслаждаться напитком даже новичкам в мире виски.\n"
            "7. Monkey Shoulder завоевал множество международных медалей, в том числе на San Francisco World Spirits Competition.\n"
            "8. Этот виски отлично проявляет себя в коктейлях Old Fashioned и Whisky Sour, добавляя им сладковато-пряный акцент.\n"
            "9. Дизайн бутылки с тремя бронзовыми «плечами» символизирует три вида солода в составе купажа.\n"
            "10. Благодаря сочетанию качества, доступной цены и модного имиджа Monkey Shoulder остаётся одним из самых продаваемых купажированных виски в мире."
        ),
    },
    "Glenfiddich 12 Years": {
        "photo": None,
        "text": (
            "1. Glenfiddich 12 — флагманский односолодовый виски семейной винокурни William Grant & Sons в регионе Спейсайд.\n"
            "2. Выдержка не менее 12 лет в бочках из американского и европейского дуба придаёт напитку мягкость и сложность.\n"
            "3. Аромат сочетает в себе ноты спелой груши, мёда и лёгкого дубового дыма.\n"
            "4. Во вкусе ощущаются сладкие дыня и яблоко, подкреплённые лёгкой пряностью и нежным дубовым послевкусием.\n"
            "5. Крепость 40% позволяет раскрыть все нюансы букета как в чистом виде, так и с добавлением капли воды.\n"
            "6. Glenfiddich 12 регулярно получает высокие оценки от экспертов на дегустациях London IWSC и San Francisco World Spirits.\n"
            "7. Его рекомендуют сочетать с блюдами из белого мяса, рыбой и мягкими сырами, чтобы подчеркнуть фруктовые ноты.\n"
            "8. Фирменная бутылка с оленем и надписью Glenfiddich стала одним из символов качественного односолодового виски.\n"
            "9. Благодаря своему балансу и доступности он идеально подходит тем, кто только знакомится с миром солодовых дистиллятов.\n"
            "10. Glenfiddich 12 остается бестселлером и «визитной карточкой» шотландского солода уже более полувека."
        ),
    },
    # --- остальные бренды виски (Fire & Cane, IPA Experiment, ... ) в том же формате ---
}

WHISKY_KB = ReplyKeyboardMarkup(
    keyboard=[kb_row(*[
        "Monkey Shoulder", "Glenfiddich 12 Years", "Fire & Cane", "IPA Experiment",
        "Grant's Classic", "Grant's Summer Orange", "Grant's Winter Dessert",
        "Grant's Tropical Fiesta", "Tullamore D.E.W.", "Tullamore D.E.W. Honey",
    ]), kb_row("Назад")],
    resize_keyboard=True,
)

# ------------------------------- Vodka -------------------------------------
# (Аналогично создаём словари VODKA_DATA, BEER_DATA, WINE_DATA и др.)
# Чтобы не загромождать пример, покажу один элемент, но в реальном файле
# вставьте ВСЕ описания без изменений.

VODKA_DATA = {
    "Серебрянка": {
        "photo": None,
        "text": (
            "1. Серебрянка — казахстанская водка, производимая на заводе в Актюбинске.\n"
            "2. Для её производства используется очищенная талая вода из местных источников.\n"
            "3. Базовым сырьём служит мягкая пшеница высокого качества.\n"
            "4. Процесс тройной ректификации обеспечивает максимальную чистоту напитка.\n"
            "5. В аромате ощущаются лёгкие зерновые ноты с намёком на нейтральность.\n"
            "6. Во вкусе доминирует кристальная чистота и мягкая текстура без острых оттенков.\n"
            "7. Крепость стандартная — 40%, что делает Серебрянку универсальной для барной карты.\n"
            "8. Этот бренд популярен на массовых мероприятиях и застольях благодаря доступной цене.\n"
            "9. Серебрянка получила несколько региональных наград за стабильное качество.\n"
            "10. Упаковка выполнена в лаконичном стиле с серебристой этикеткой, подчёркивающей её название."
        ),
    },
    # ... остальные водочные бренды ...
}

VODKA_KB = ReplyKeyboardMarkup(
    keyboard=[kb_row("Серебрянка", "Reyka", "Finlandia"),
              kb_row("Русский стандарт", "Зелёная марка", "Талка"),
              kb_row("Назад")],
    resize_keyboard=True,
)

# ----------------------------  Хендлеры  -----------------------------------

@router.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer("Привет! Выбери категорию:", reply_markup=CATEGORY_KB)

# --- возврат в главное меню ---
@router.message(Text("Назад"))
async def go_back(message: Message):
    await send_welcome(message)

# --- категории ---
@router.message(Text("🥃 Виски"))
async def category_whisky(message: Message):
    await message.answer("🥃 Выбери бренд виски:", reply_markup=WHISKY_KB)

@router.message(Text(list(WHISKY_DATA.keys())))
async def whisky_brands(message: Message):
    data = WHISKY_DATA[message.text]
    if data.get("photo"):
        await message.answer_photo(photo=data["photo"], caption=data["text"])
    else:
        await message.answer(data["text"])

# --- Водка ---
@router.message(Text("🧊 Водка"))
async def category_vodka(message: Message):
    await message.answer("🧊 Выберите бренд водки:", reply_markup=VODKA_KB)

@router.message(Text(list(VODKA_DATA.keys())))
async def vodka_brands(message: Message):
    data = VODKA_DATA[message.text]
    if data.get("photo"):
        await message.answer_photo(photo=data["photo"], caption=data["text"])
    else:
        await message.answer(data["text"])

# ---------------------------------------------------------------------------
#               (Добавьте аналогичные блоки для Пива, Вина, Ягера)
# ---------------------------------------------------------------------------

# --------------------------   Тесты  ---------------------------------------
#   логика тестов перенесена без изменений, только декораторы заменены

TEST_QUESTIONS = {  # полностью скопируйте ваш словарь вопросов сюда
    # ...
}

user_tests: dict[int, dict] = {}

@router.message(Text("📋 Тесты"))
async def tests_menu(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            kb_row("🧪 Тест по Jägermeister", "🥃 Тест по Виски"),
            kb_row("🧊 Тест по Водке", "🍺 Тест по Пиву"),
            kb_row("🍷 Тест по Вину"),
            kb_row("Назад"),
        ],
        resize_keyboard=True,
    )
    await message.answer("Выберите тест:", reply_markup=kb)

# вспомогательные функции тестов (init_test, send_question) оставляем теми же
# только заменяем ReplyKeyboardMarkup / Remove импортов – уже импортированы выше

# --------------------------  Запуск  ---------------------------------------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
