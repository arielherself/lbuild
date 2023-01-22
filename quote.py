import time
import random
import os
import telebot
import local_secret

LANG = 'zh'
MIN_LENGTH = 20

TOKEN = local_secret.LBUILD_QUOTE_BOT_TOKEN

def quote():
    random.seed(time.time())
    filename = random.choice(os.listdir(f'./data/{LANG}/'))
    with open(f'./data/{LANG}/{filename}', encoding='utf8') as f:
        lines = [l.strip() for l in f.readlines()]
    lines = list(filter(lambda s: len(s) >= MIN_LENGTH, lines))
    random.seed(time.time())
    return random.choice(lines)

bot = telebot.TeleBot(TOKEN)
print('Ready.')

@bot.message_handler(commands=['quote'])
def reply(message):
    print('Received a request.')
    try:
        bot.reply_to(message, quote())
    except Exception as e:
        print('Aborted with error:', e)
    else:
        print('Replied.')

if __name__ == '__main__':
    bot.polling()
