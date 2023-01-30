import time
import datetime
import random
import os
import asyncio
import telebot
from telebot.async_telebot import AsyncTeleBot
import local_secret

LANG = 'zh'
MIN_LENGTH = 20
PUSH_GROUPS = ('5302591220', '-1001529721824',)

TOKEN = local_secret.LBUILD_QUOTE_BOT_TOKEN

flag = True

def quote():
    try:
        random.seed(time.time())
        filename = random.choice(os.listdir(f'./data/{LANG}/'))
        with open(f'./data/{LANG}/{filename}', encoding='utf8') as f:
            lines = [l.strip() for l in f.readlines()]
        lines = list(filter(lambda s: len(s) >= MIN_LENGTH, lines))
        random.seed(time.time())
        return random.choice(lines)
    except:
        return quote()

bot = AsyncTeleBot(TOKEN)
print('Ready.')

@bot.inline_handler(lambda _: True)
async def inline_reply(inline_query):
    print('Received a request.')
    try:
        r1Text = f'{inline_query.query}\n\n{"="*10}\n<i>"{quote()}"</i>'
        r2Text = f'{str(datetime.date.today())}\n{inline_query.query}\n\n{"="*10}\n<i>"{quote()}"</i>'
        r1 = telebot.types.InlineQueryResultArticle('1', '便笺', telebot.types.InputTextMessageContent(r1Text, 'html'), description=r1Text)
        r2 = telebot.types.InlineQueryResultArticle('2', '带日期的便笺', telebot.types.InputTextMessageContent(r2Text, 'html'), description=r2Text)
        await bot.answer_inline_query(inline_query.id, [r1, r2])
    except Exception as e:
        print('Aborted with an error:', e)
    else:
        print('Replied.')

@bot.message_handler(commands=['quote'])
async def reply(message):
    print('Received a request.')
    try:
        await bot.reply_to(message, quote())
    except Exception as e:
        print('Aborted with an error:', e)
    else:
        print('Replied.')

async def autoPost():
    global flag
    while True:
        if datetime.datetime.now().hour == 11:
            if flag:
                m = f'{str(datetime.date.today())} #晚上好\n\n<i>"{quote()}"</i>'
                for groupID in PUSH_GROUPS:
                    await bot.send_message(groupID, m, 'html')
                flag = False
            else:
                pass
        elif datetime.datetime.now().hour == 16:
            if flag:
                m = f'{str(datetime.date.today())} #早上好\n\n<i>"{quote()}"</i>'
                for groupID in PUSH_GROUPS:
                    await bot.send_message(groupID, m, 'html')
                flag = False
            else:
                pass
        elif datetime.datetime.now().hour == 23:
            if flag:
                with open('./data/hello.wav', 'rb') as f:
                    for groupID in PUSH_GROUPS:
                        await bot.send_audio(groupID, f, '起床啦！', 13, 'cc', '早上好', protect_content=True)
                flag = False
            else:
                pass
        else:
            flag = True
        await asyncio.sleep(20)

async def main():
    t1 = asyncio.create_task(bot.polling(non_stop=True, timeout=180))
    t2 = asyncio.create_task(autoPost())
    await t1
    await t2

if __name__ == '__main__':
    asyncio.run(main())
