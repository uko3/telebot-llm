#GigaChat
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat



from telebot.async_telebot import AsyncTeleBot
import telebot
import requests
from telebot import types
import asyncio

#from gigachat import GigaChat
#from gigachat.models import Chat, Messages, MessagesRole



bot = AsyncTeleBot('')
cnt_tokens = 350

giga = GigaChat(credentials='', scope='GIGACHAT_API_PERS', verify_ssl_certs=False, max_tokens=cnt_tokens)

expert_promt_tim = 'Ты эксперт бот, который помогает пользователю решить его проблемы'
expert_promt_gig = 'Ты эксперт бот, который хорошо умеет программировать по всем необходимым стандартам'
expert_promt_kot = 'Ты эрудированный бот, который понятно объясняет сложные темы'



tim_messages = [
  SystemMessage(
    content=expert_promt_tim
  )
]

gig_messages = [
  SystemMessage(
    content=expert_promt_gig
  )
]

kot_messages = [
  SystemMessage(
    content=expert_promt_kot
  )
]

messages_history = []
bot_name = 'Bot'

def answer(topic, messages, bot_name):
    messages.append(HumanMessage(content=topic))
    res = giga(messages)
    messages.append(res)

    return bot_name + ':' + res.content




@bot.message_handler(commands=['start'])
async def start2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    await bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник! Я помогу с проектом", reply_markup=markup)



@bot.message_handler(content_types='text')
async def get_text_messages(message: types.Message):

    global messages_history, bot_name
    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
        btn1 = types.KeyboardButton('Тим:Варианты решений')
        btn2 = types.KeyboardButton('Гиг:Написать код')
        btn3 = types.KeyboardButton('Кот:Изучить темы')
        markup.add(btn1, btn2, btn3)
        await bot.send_message(message.from_user.id, '❓ Выберити раздел и задайте интересующий вас вопрос', reply_markup=markup) #ответ бота

    elif message.text == 'Тим:Варианты решений':
        bot_name = 'Тим'
        messages_history = tim_messages
        await bot.send_message(message.from_user.id, answer( topic = message.text, messages = messages_history, bot_name = bot_name), parse_mode='Markdown')

    elif message.text == 'Гиг:Написать код':
        bot_name = 'Гиг'
        messages_history = gig_messages
        await bot.send_message(message.from_user.id, answer( topic = message.text, messages = messages_history, bot_name = bot_name), parse_mode='Markdown')

    elif message.text == 'Кот:Изучить темы':
        bot_name = 'Кот'
        messages_history = kot_messages
        await bot.send_message(message.from_user.id, answer( topic = message.text, messages = messages_history, bot_name = bot_name), parse_mode='Markdown')


    else: await bot.send_message(message.from_user.id, answer(topic = message.text, messages = messages_history, bot_name = bot_name), parse_mode='Markdown' )
   



asyncio.run(bot.polling())


