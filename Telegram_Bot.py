import os 
from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CRYPTO_NAME_TO_PICKER = {
    "Bitcoin": "BTCUSDT",
    "Etherium": "ETHUSDT",
    "Doge": "DOGEUSDT"
}

bot = TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=3)
    for crypto_name in CRYPTO_NAME_TO_PICKER.keys():
        item_button = KeyboardButton(crypto_name)
        markup.add(item_button)
    bot.send_message(message.chat.id, "choose a cryptovalue", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in CRYPTO_NAME_TO_PICKER.keys())
def send_price(message):
    crypto_name = message.text
    print(crypto_name)
    ticker = CRYPTO_NAME_TO_PICKER[crypto_name]
    price = get_price_by_ticker(ticker=ticker)
    bot.send_message(message.chat.id, f"Price of {crypto_name} to USDT is {price}")


def get_price_by_ticker(*, ticker:str) -> float:
    endpoint = "https://api.binance.com/api/v3/ticker/price"
    params ={
        'symbol': ticker,
    }
    response = requests.get(endpoint, params=params)
    data = response.json()
    price = round(float(data["price"]), 2)
    return price

bot.infinity_polling()