import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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

# Списки валютных пар
standard_currencies = ["CHF/JPY", "AUD/NZD", "EUR/USD", "EUR/JPY", "AUD/CAD", "AUD/JPY", "GBP/NZD", "USD/CAD"]
otc_currencies = ["EUR/USD (OTC)", "NZD/JPY (OTC)", "GBP/JPY (OTC)", "AUD/JPY (OTC)", "EUR/JPY (OTC)", "CHF/JPY (OTC)"]

# Состояние выбора валют
user_state = {}

# Функция для получения локализованного сообщения
def get_message(language_code, key):
    return localizations.get(language_code, localizations["en"]).get(key, "")

# Генерация клавиатуры с выбором стандартных или OTC валют
def generate_currency_keyboard(currencies):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for currency in currencies:
        markup.add(KeyboardButton(currency))
    markup.add(KeyboardButton('🔙 Back'))
    return markup

# Стартовая клавиатура
def main_menu_keyboard(language_code):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(get_message(language_code, "choose_currency_pair")),
        KeyboardButton(get_message(language_code, "choose_currency_pair_otc"))
    )
    return markup

# Команда /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    language_code = message.from_user.language_code
    await message.answer(
        get_message(language_code, "start_message"),
        reply_markup=main_menu_keyboard(language_code)
    )

# Обработка текстовых сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    language_code = message.from_user.language_code
    text = message.text

    if text in [get_message(language_code, "choose_currency_pair"), get_message(language_code, "choose_currency_pair_otc")]:
        if text == get_message(language_code, "choose_currency_pair"):
            user_state[message.from_user.id] = 'standard'
            await message.answer(get_message(language_code, "current_pairs"), reply_markup=generate_currency_keyboard(standard_currencies))
        else:
            user_state[message.from_user.id] = 'otc'
            await message.answer(get_message(language_code, "current_pairs_otc"), reply_markup=generate_currency_keyboard(otc_currencies))

    elif text in standard_currencies + otc_currencies:
        arrow = random.choice(["UP⬆️", "DOWN⬇️"])
        await message.answer(f"{text}: {arrow}")

        # После ответа предлагаем снова выбрать
        await message.answer(
            get_message(language_code, "select_currency_pair"),
            reply_markup=main_menu_keyboard(language_code)
        )

    elif text == "🔙 Back":
        # Кнопка Назад
        await message.answer(
            get_message(language_code, "start_message"),
            reply_markup=main_menu_keyboard(language_code)
        )

    else:
        # На неизвестные команды
        await message.answer("⚠️ Unknown command. Please use buttons.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
