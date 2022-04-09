import vk_api
from mctools import RCONClient  # Import the RCONClient
from vk_api.longpoll import VkLongPoll, VkEventType
from mcstatus import MinecraftServer, querier
import slovarik
from slovarik import *
from mctools import errors
from time import sleep

group_token = grouptoken
my_token = mytoken

grt = vk_api.VkApi(token=group_token)  # берём токен группы
myt = vk_api.VkApi(token=my_token)  # берём ваш токен
give = grt.get_api()  # берём апи из токена группы
give2 = myt.get_api()  # берём апи из вашего токена
longpoll = VkLongPoll(grt)  # подключаемся к вк пулу с помощью токена группыы


def sendmessage(id, text):
    grt.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


# определяем метод sendmessage который принимает значение id и text, и отправляет text человеку с айди id

def rconcommand(com, vid):
    if id in adminsid:
        try:
            command = rcon.command(com)
        except Exception as eror:
            sendmessage(vid, f'Не удалось выполнить команду по причине {eror}')
        else:
            sendmessage(vid, f'Выполнил команду {com}, '
                             f'Вывод команды: {command}')
    else:
        sendmessage(vid, 'Ты не админ!')


def banplayer(message, id):
    if id in adminsid:  # если айди не в массиве айди админом
        if 3 < len(message.split(" ")) < 5:  # аахахахах если слов в сообщении больше 3 но меньше 5
            nick = message.split(" ")[1]  # записывает ник
            time = message.split(" ")[2]  # записывает на какое время забанить
            reason = message.split(" ")[3]  # записаывает причину
            com1 = rcon.command(f"tempban {nick} {time} {reason}")  # и банит по всем трём параметрам
            if 'Ошибка' in com1:
                sendmessage(id, f'Произошла ошибка при бане игрока {nick}. Игрок существует? Команда написана '
                                f'правильно?')  # и если ошибка при вводе сообщения на сервер то выводит вот так
            else:
                sendmessage(id, f'Забанил {nick} на {time} по причине {reason}')
        elif len(message.split(" ")) == 3:  # если слов в сообщении 3
            nick = message.split(" ")[1]  # записывает ник
            reason = message.split(" ")[2]  # и причину
            com1 = rcon.command(f'ban {nick} {reason}')  # и банит перманентно
            if 'Ошибка' in com1:
                sendmessage(id, f'Произошла ошибка при бане игрока {nick}. Игрок существует? Команда написана '
                                f'правильно?')
            else:
                sendmessage(id, f'Перманентно забанил {nick} по причнине {reason}')
        else:
            sendmessage(id, 'Команда "бан" введена неправильно. Возможно не написана причина? '
                            'Правильное написание команды: бан {игрок} {время} {причина} для временного бана, '
                            'и бан {игрок} {причина} для перманентного бана')  # ну если чето напутали вот так кароче
    else:
        sendmessage(id, 'Ты не админ!')


try:  # пробуем выполнить тело кода
    server = MinecraftServer.lookup(f'{serverip}:{serverport}')  # в переменную server засовываем ваш сервер
    HOST = serverip  # айпишник сервера без порта для ркона
    PORT = rconport  # порт ркона, НЕ СЕРВЕРА
    rcon = RCONClient(HOST, port=PORT)  # подключаемся к ркону
    connect = rcon.login(rconPass)  # вводим пароль ркона
except Exception as error:  # если вылезла ошибка (например сервер лежит и не отвечает) пишем админу причину
    sendmessage(myvkid, f'Ошибка подключения к серверу по причине {error}!')
else: sendmessage(myvkid, 'Бот успешно запущен!')

# Слушаем longpoll(Сообщения)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        # Чтобы наш бот не слышал и не отвечал на самого себя
        if event.to_me:
            # Для того чтобы бот читал все с маленьких букв
            message = event.text.lower()
            # Получаем id пользователя
            id = event.user_id

            if message.split(" ")[
                0] in ping:  # если в сообщении которое отправил челикс ПЕРВОЕ слово это одно из массива ping
                try:
                    latency = server.ping()  # пробуем пингануть сервер
                    status = server.status()  # пробуем узнать статус сервера
                except Exception as e:  # если вылезла ошибка
                    sendmessage(id,
                                f'Сервер не отвечает по причине {e}. Свяжитесь с админом как можно скорее.')  # отправляем пользователю это сообщение чтобы скрипт не выключился
                else:  # если нет ошибок
                    sendmessage(id,
                                f'Пинг: {latency} мс, на сервере сейчас {status.players.online} игрока(ов)')  # пишем это
                    # вся эта хуйня показывает пинг сервера                   и кол-во игроков

            elif message.split(" ")[
                0] in players:  # если в сообщении которое отправил челикс ПЕРВОЕ слово это одно из массива players
                com1 = rcon.command("list")  # отправляем на сервер команду /list
                com1 = com1.replace("[0m", "")  # убираем из полученого результата ненужные символы
                sendmessage(id, com1)  # пишем пользователю это



            elif message.split(" ")[0] in whitelist:  # если ПЕРВОЕ СЛОВО это одно из списка 'whitelist', то
                if id in adminsid:
                    if len(message.split(" ")) > 1:  # проверяем является ли айди написавшего - вашим
                        if message.split(" ")[1] == 'добавить':  # проверяем что ВТОРОЕ СЛОВО - добавить
                            com1 = rcon.command("whitelist add " + message.split(" ")[
                                2])  # отправляем ркон команду на добавление вайтлиста с третьим словом в сообщении пользователя
                            sendmessage(id, f'Добавил {message.split(" ")[2]} в вайтлист')  # сообщаем что всё хорошо
                        elif message.split(" ")[1] == 'удалить':  # если же ВТОРОЕ СЛОВО - удалить
                            com1 = rcon.command("whitelist remove " + message.split(" ")[
                                2])  # отправляем ркон команду на удаление из вайтлиста с третьим словом в сообщении пользователя
                        if 'Player is not whitelisted' in com1:
                            sendmessage(id,
                                        f'Не удалось удалить {message.split(" ")[2]} из вайтлиста. Был ли он в нём вообще?')
                        else:
                            sendmessage(id, f'Удалил {message.split(" ")[2]} из вайтлиста')  # сообщаем что всё хорошо
                    else:
                        sendmessage(id,
                                    'Нужно написать команду вида "Вайтлист {добавить/удалить} {никнейм}"')  # если написали "вайтлист" но другие слова неправильные, то выведт это сообщение
                else:
                    sendmessage(id, 'Ты не админ или команда введена неправильно!')

            elif message.split(" ")[0] in ban:  # если введеное сообщение содержит в себе слово из массива бан
                banplayer(message, id)  # выполняем функцЫю, она сверху

            elif message.split(" ")[0] in unban:  # если из массива анбан
                if id in adminsid:  # если айди в списке айди админом
                    nick = message.split(" ")[1]  # берём ник за переменную, зачем не знаю ахахаахха
                    com1 = rcon.command(f"pardon {nick}")
                    if 'Ошибка' in com1:  # если в выводе команды ошибка, то пишем это написавшему
                        sendmessage(id,
                                    f'Произошла ошибка при разбане игрока {nick}. Игрок существует? Команда написана '
                                    f'правильно?')
                    else:
                        sendmessage(id, f'Разбанил игрока {nick}')  # ну а если нет то разбаниваем
                else:
                    sendmessage(id, 'Ты не админ!')

            elif message.split(" ")[0] in kick:  # ну тут кикает кароче, принимает либо 3 значения, либо 2
                if id in adminsid:
                    if len(message.split(" ")) == 3:  # если 3 слова введено - кикает игрока с причиной
                        com1 = rcon.command(f'kick {message.split(" ")[1]} {message.split(" ")[2]}')
                        if 'Invalid name or UUID' in com1:  # проверяет есть ли ошибка в нике
                            sendmessage(id, f'Не удалось кикнуть. Такого игрока нет, либо ник написан неправильно')
                        else:
                            sendmessage(id,
                                        f'Кикнул {message.split(" ")[1]} по причине {message.split(" ")[2]}, вывод {com1}')
                    elif len(message.split(" ")) == 2:  # два слова - кикает без причины
                        com1 = rcon.command(f'kick {message.split(" ")[1]}')
                        if 'Invalid name or UUID' in com1:  # проверяет есть ли ошибка в нике
                            sendmessage(id, f'Не удалось кикнуть. Такого игрока нет, либо ник написан неправильно')
                        else:
                            sendmessage(id, f'Кикнул {message.split(" ")[1]} без причины, вывод {com1}')
                    else:  # ну и если слов не 3 и не 2 то выводит это
                        sendmessage(id, 'Не удалось кикнуть. Написана ли причина? Причина состоит больше чем из одного '
                                        'слова?')
                else:
                    sendmessage(id, 'Ты не админ!')

            elif message.split(" ")[0] in tp:
                if id in adminsid:
                    if len(message.split(" ")) == 5:
                        player = message.split(" ")[1]
                        x = message.split(" ")[2]  # ну кароче вкратце он в переменные кладёт определенные слова
                        y = message.split(" ")[3]  # тоесть написал ты боту "тп игрок 10 10 10", и он распределит
                        z = message.split(" ")[4]  # все эти значения, но только если не больше 5 слов в сообещнии
                        com1 = rcon.command(f'tp {player} {x} {y} {z}')
                        sendmessage(id,
                                    f'Телепортировал {player} на координаты x{x} y{y} z{z}')  # ну а здесь он тпает исходя из переменных
                    else:
                        sendmessage(id, 'Команда телепорта введена неправильно. Нужно: tp НИК X Y Z')
                else:
                    sendmessage(id, 'Ты не админ!')

            elif message.split(" ")[0] == 'всем:':
                if id in adminsid:
                    com1 = rcon.command(
                        f'broadcast {message.replace("всем:", "")}')  # просто шлёт всем сообщение через команду /broadcast, она в essentials
                    sendmessage(id,
                                f'Написал на сервер собщение: {message.replace("всем:", "")}')  # можно заменить /tellraw @a "{message.replace("всем:","")}", одна хуйня получится
                else:
                    sendmessage(id, 'Ты не админ!')

            elif message.split(" ")[0] in donate:  # выдать донат посредством LuckPerms
                if id in adminsid:
                    if len(message.split(" ")) == 4:
                        com1 = rcon.command(
                            f'lp user {message.split(" ")[1]} parent addtemp {message.split(" ")[2]} {message.split(" ")[3]}')
                        sendmessage(id, f'Выдал привелегию {message.split(" ")[2]} игроку {message.split(" ")[1]} '
                                        f'на {message.split(" ")[3]}, вывод команды: {com1}')
                    elif len(message.split(" ")) < 4:
                        sendmessage(id, 'Команда введена неправильно, отсутствуют '
                                        'параметры. Правильно: выдатьдонат '
                                        '{название привелегии} {игрок} {время}')
                    elif len(message.split(" ")) > 4:
                        sendmessage(id, 'Слишком много параметров! Правильно: выдатьдонат '
                                        '{название привелегии} {игрок} {время}')
                else:
                    sendmessage(id, 'Ты не админ!')

            elif message[0] == 'донат':
                sendmessage(id,f'Вы можете приобрести донат здесь: {donatelink}')
            elif message.split(" ")[0] == 'команда':  # отправить команду ркон если её нет в этом скрипте чреез слеш
                rconcommand(message.replace("команда", ""), id)
                # то что ниже ломает бота если человек отправил стикер
          #  elif message[0] == '!':  # если первый СИМВОЛ сообщения - !, то перенаправляем сообщение админу
         #       sendmessage(id, f'Передал админу. Вообще было бы легче если бы ты написал ему лично: @{myvkid}')
         #       for i in range(len(adminsid)):
           #         sendmessage(adminsid[i], f'@id{str(id)} написал: {message.replace("!", "")}')

            elif message.split(" ")[0] == 'пися':  # это просто ржака
                sendmessage(id, 'попа')

            else:  # если ничего из этого списка не было написано - пишет вот это
                sendmessage(id, f'Неизвестная команда. Если у вас есть вопрос, то пишите админу @{myvkid}')

# код карчое являестя собственостью серёжи юдина vk.com/szarkan, не воруйте пожалуйста !!!
