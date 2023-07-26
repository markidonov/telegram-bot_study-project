from django.core.management.base import BaseCommand
from tgb.models import *
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import Bot, ReplyKeyboardMarkup
from telegram.utils.request import Request
import requests
import random
import os

updater = Updater(token=os.getenv('bot_token'))
URL_news = f'https://api.thenewsapi.com/v1/news/all?locale=ru&language=ru&limit=3&api_token={os.getenv("api_key_news")}'
URL_weather = f'https://api.openweathermap.org/data/2.5/weather?lang=ru&units=metric&appid={os.getenv("api_key_weather")}'


def save_message(update, context):
    c, _ = Client.objects.get_or_create(tg_id=update.message.chat_id,
    defaults={'name': update.message.chat.username})
    m = Message(client=c, text=update.message.text)
    m.save()


def news(update, context):
        response = requests.get(
            f'{URL_news}&categories={random.choice(["tech", "sports", "science"])}').json()
        random_new = response.get('data')[random.randint(0, 2)].get('url')
        chat = update.effective_chat
        save_message(update, context)
        context.bot.send_message(chat.id, random_new)


def weather_tomsk(update, context):
    response = requests.get(f'{URL_weather}&q=Tomsk').json()
    name = response['name']
    temp = response['main']['temp']
    desc = response['weather'][0]['description']
    chat = update.effective_chat
    save_message(update, context)
    context.bot.send_message(chat.id, f'Запрашиваемая территория: {name} ')
    context.bot.send_message(chat.id, f'Температура: {temp} градусов по Цельсию')
    context.bot.send_message(chat.id, f'Погодные условия: {desc} ')


def weather_any(update, context):
    chat = update.effective_chat
    text = update.message.text.split()
    if text[0]=='/weather':
        try:    
            url = f'{URL_weather}&q={text[1]}'
            response = requests.get(url).json()
            name = response['name']
            temp = response['main']['temp']
            desc = response['weather'][0]['description']
            chat = update.effective_chat
            save_message(update, context)
            context.bot.send_message(chat.id, f'Запрашиваемая территория: {name} ')
            context.bot.send_message(chat.id, f'Температура: {temp} градусов по Цельсию')
            context.bot.send_message(chat.id, f'Погодные условия: {desc} ')
        except:
            context.bot.send_message(chat.id, 'Проверьте название города, оно должно быть '
                                                'через пробел указано на английском')
    else:
        context.bot.send_message(chat_id=chat.id,
                            text='Вы ввели неизвестную команду,'
                                'для просмотра команд введите "/help"')


def admin_commands():
    o = Order.objects.values('command')
    list_order = [x for x in o]
    return list_order


def start_bot(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    save_message(update, context)
    list_true = []
    for x in admin_commands():
        list_true.append(['/'+x['command']])
    button = ReplyKeyboardMarkup(
            [['/help', '/news'],
            ['/weather_tomsk']] + list_true 
        , resize_keyboard=True)
    context.bot.send_message(chat_id=chat.id, 
                                text='Уважаемый(ая) {}, Вас приветствует тестовый бот.'
                                    'Я могу рассказать вам о погоде или '
                                    'последние новости. Для просмотра команд '
                                    'используйте /help'.format(name),
                                reply_markup=button)


def help_me(update, context):
    chat = update.effective_chat
    save_message(update, context)
    list_true = []
    for x in admin_commands():
        list_true.append('/'+x['command'])
    context.bot.send_message(chat_id=chat.id, text='Доступные команды: ')
    context.bot.send_message(chat_id=chat.id, text='/start')
    context.bot.send_message(chat_id=chat.id, text='/news')  
    context.bot.send_message(chat_id=chat.id, text='/weather <город по-английски>')  
    for i in list_true:
        context.bot.send_message(chat_id=chat.id, text=i)


def admins(update, context):
    chat = update.effective_chat
    object = Order.objects.get(command=update.message.text[1:])
    answer = str(object).split() 
    res = " ".join(answer[2: len(answer)])
    save_message(update, context)
    context.bot.send_message(chat_id=chat.id, 
                                text=res)
    

class Command(BaseCommand):
    help = 'Телеграм-бот'
    
    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot=Bot(request=request,
                token=os.getenv('bot_token'))
        
    
    # Отлавливаем команды от админов
    list_true = []
    for x in admin_commands():
        list_true.append(x['command'])
    for i in list_true:
        updater.dispatcher.add_handler(CommandHandler(i, admins))

    # Отлавливаем "базовые" команды     
    list_commands = ['news', 'start', 'help', 'weather_tomsk',]
    list_funcs = [news, start_bot, help_me, weather_tomsk,] 
    for i in range(0, len(list_funcs)):
        updater.dispatcher.add_handler(CommandHandler(list_commands[i], list_funcs[i]))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, weather_any))
    
    updater.start_polling()
    updater.idle() 
