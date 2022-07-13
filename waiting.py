import os
import sys
from slovarik_minecraft import *
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

group_t = vk_api.VkApi(token=grouptoken)  # берём токен группы
my_t = vk_api.VkApi(token=mytoken)  # берём ваш токен
give = group_t.get_api()  # берём апи из токена группы
give2 = my_t.get_api()  # берём апи из вашего токена
longpoll = VkLongPoll(group_t)  # подключаемся к вк пулу с помощью токена группыы

def sendmessage(id, text):
    group_t.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})
# определяем метод sendmessage который принимает значение id и text, и отправляет text человеку с айди id

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        # Чтобы наш бот не слышал и не отвечал на самого себя
        if event.to_me:
            # Для того чтобы бот читал все с маленьких букв
            message = event.text
            args = message.split(" ")
            # Получаем id пользователя
            id = event.user_id
            if args[0] == 'включи': # пишем включи - он включает основной скрипт, а сам уходит спать
                if id in adminsid:
                    os.system("python3 vkbot.py")
                    sys.exit(0)
                else:
                    sendmessage(id, 'Ты не админ.')
            elif 'умер' in message: # если игроки напишут типа "бот умер", то он ответи забавной фразочкой
                sendmessage(id, 'Это лишь временно :)')
            else: # на любые особщения в его адрес (кроме верхних двух) он ответит вот это
                sendmessage(id, 'Привет. Это аварийная версия бота, которая может делать ровным счётом ничего.\n'
                                'Возможно основной бот на тех. работах, поэтому ожидай его скорейшего включения :)')