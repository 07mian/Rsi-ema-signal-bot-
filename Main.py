import time
import telebot
from config import BOT_TOKEN, CHAT_ID, PAIR_OPTIONS
from signal_scraper import get_signal

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "📊 RSI + EMA Signal Bot Started")
    for pair in PAIR_OPTIONS:
        signal = get_signal(pair)
        bot.send_message(message.chat.id, signal)

def auto_loop():
    while True:
        for pair in PAIR_OPTIONS:
            signal = get_signal(pair)
            bot.send_message(CHAT_ID, signal)
            time.sleep(2)
        time.sleep(60)

# Optional: run automatically every minute
# auto_loop()

bot.polling()
