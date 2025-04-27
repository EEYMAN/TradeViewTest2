import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = '8178668402:AAHhnaR4idzlp1Nglg9FmsrIM8uci4OydW4'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Локализованные строки
localizations = {
    "en": {
        "start_message": "Choose an active currency pair",
        "choose_currency_pair": "Choose current pair",
        "choose_currency_pair_otc": "Choose current pair (OTC)",
        "current_pairs": "Current currency pairs:",
        "current_pairs_otc": "Current currency pairs (OTC):",
        "select_currency_pair": "Select a currency pair",
    },
    "ru": {
        "start_message": "Начать торговлю",
        "choose_currency_pair": "Выбрать валютную пару",
        "choose_currency_pair_otc": "Выбрать валютную пару (OTC)",
        "current_pairs": "Актуальные валютные пары:",
        "current_pairs_otc": "Актуальные валютные пары (OTC):",
        "select_currency_pair": "Выберите валютную пару",
    }
}

# Функция для получения локализованного сообщения
def get_message(language_code, key):
    return localizations.get(language_code, localizations["en"]).get(key, "")

# Команда /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    language_code = message.from_user.language_code
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(get_message(language_code, "choose_currency_pair"), callback_data="choose_currency_pair"),
        InlineKeyboardButton(get_message(language_code, "choose_currency_pair_otc"), callback_data="choose_currency_pair_otc")
    )
    await bot.send_message(message.chat.id, get_message(language_code, "start_message"), reply_markup=markup)

# Обработчик выбора типа валютной пары
@dp.callback_query_handler(lambda c: c.data in ["choose_currency_pair", "choose_currency_pair_otc"])
async def choose_currency_pair(callback_query: types.CallbackQuery):
    language_code = callback_query.from_user.language_code
    data = callback_query.data

    # Определяем список валютных пар в зависимости от выбора пользователя
    if data == "choose_currency_pair":
        currencies = ["CHF/JPY", "AUD/NZD", "EUR/USD", "EUR/JPY", "AUD/CAD", "AUD/JPY", "GBP/NZD", "USD/CAD"]
        message_key = "current_pairs"
    else:  # choose_currency_pair_otc
        currencies = ["EUR/USD (OTC)", "NZD/JPY (OTC)", "GBP/JPY (OTC)", "AUD/JPY (OTC)", "EUR/JPY (OTC)", "CHF/JPY (OTC)"]
        message_key = "current_pairs_otc"

    markup = InlineKeyboardMarkup(row_width=2)
    for currency in currencies:
        markup.add(InlineKeyboardButton(currency, callback_data=f"currency_{currency}"))

    await bot.edit_message_text(
        get_message(language_code, message_key),
        callback_query.message.chat.id,
        callback_query.message.message_id,
        reply_markup=markup
    )

# Обработчик выбора конкретной валютной пары
@dp.callback_query_handler(lambda c: c.data.startswith("currency_"))
async def show_random_arrow(callback_query: types.CallbackQuery):
    currency = callback_query.data.split("_", 1)[1]
    language_code = callback_query.from_user.language_code
   arrow = random.choice(["UP", "DOWN"])
    
    await bot.send_message(callback_query.message.chat.id, f"{currency}: {arrow}")

    # Возвращаем кнопки выбора валютных пар
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(get_message(language_code, "choose_currency_pair"), callback_data="choose_currency_pair"),
        InlineKeyboardButton(get_message(language_code, "choose_currency_pair_otc"), callback_data="choose_currency_pair_otc")
    )

    await bot.send_message(callback_query.message.chat.id, get_message(language_code, "select_currency_pair"), reply_markup=markup)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
