import vk_api
from mctools import RCONClient, errors
from vk_api.longpoll import VkLongPoll, VkEventType
from mcstatus import MinecraftServer
from slovarik import *
import sys
import os
import datetime
from time import sleep
import random
import pickle
import numpy as np

group_t = vk_api.VkApi(token=grouptoken)  # берём токен группы
my_t = vk_api.VkApi(token=mytoken)  # берём ваш токен
give = group_t.get_api()  # берём апи из токена группы
give2 = my_t.get_api()  # берём апи из вашего токена
longpoll = VkLongPoll(group_t)  # подключаемся к вк пулу с помощью токена группыы
try_count = 0
read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item()
print(read_dictionary)

now = datetime.datetime.now()
now = now.strftime("%d-%m-%Y %H:%M:%S")  # делает кароче переменную now - форматированным временем (в логи посмотришь, увидишь)

def writeLog(str): # функция чтобы в логи писать
    with open('log.txt', 'a') as log: # открывает файл (если нет файла - создает)
        log.write(f'{now} - {str}\n') # пишет дату, и через тире сообщение

writeLog('='*50 + '\n' + f'{now} - Начал работу')
# вот и пример. Пишет 50 знаков "=" и на следующей строчке сообщение Начал работа

def sendmessage(id, text):
    group_t.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})
# определяем метод sendmessage который принимает значение id и text, и отправляет text человеку с айди id

def pmessage(id): # тут узнавать имя фамилию по айди
    user = group_t.method("users.get", {"user_ids": id})  # вместо 1 подставляете айди нужного юзера
    fullname = user[0]['first_name'] + ' ' + user[0]['last_name']
    return fullname

def getId(str): # ну тут кароче узнавать айди ВК по короткому именем
    if len(str) == 0:
        sendmessage(id, 'Пустая строка!')
    else:
        user = group_t.method("utils.resolveScreenName", {"screen_name": str})
        return user['object_id']


while try_count < 3:
    try:  # пробуем выполнить тело кода
        sendmessage(myvkid, 'Подключаемся к РКОНу...')
        rcon = RCONClient(serverip, port=rconport)  # подключаемся к ркону
        connect = rcon.login(rconPass)  # вводим пароль ркона
        sendmessage(myvkid, 'Пингуем сервер...')
        server = MinecraftServer.lookup(f'{serverip}:{serverport}')  # в переменную server засовываем ваш сервер
    except Exception as error:  # если вылезла ошибка (например сервер лежит и не отвечает) пишем админу причину
        sendmessage(myvkid, f'Ошибка подключения к серверу по причине: {error}! \nПопробую переподключиться...')
        writeLog(f'ОШИБКА ЗАПУСКА: {error}')
        try_count += 1
        sleep(5)
    else:
        sendmessage(myvkid, f'К РКОНу подключился! Сервер отвечает на запросы с задержкой {server.ping()}мс. '
                            f'Бот успешно запущен!')
        writeLog('Подключился к серверу')
        break
else:
    sendmessage(myvkid, f'Три попытки переподключиться к серверу оказались безуспешными. Выключаюсь.')
    writeLog('Выключаюсь из-за неудачного запуска')
    sys.exit(0)  # выключаем программу

def rconcommand(com, vid):  # просто отправляет ркон команду и пишет вывод команды
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
    if id in adminsid:  # если айди не в массиве айди админов
        args = message.split(" ")
        if 3 < len(args):  # аахахахах если слов в сообщении больше 3 но меньше 5
            nick = args[1]  # записывает ник
            time = args[2]  # записывает на какое время забанить
            r = args[3:]  # разделяет причину от других слов в сообщении
            reason = ' '.join(r)  # записаывает причину
            com = rcon.command(f"tempban {nick} {time} {reason}")  # и банит по всем трём параметрам
            if 'Ошибка' in com:
                sendmessage(id, f'Произошла ошибка при бане игрока {nick}. Игрок существует? Команда написана '
                                f'правильно?')  # и если ошибка при вводе сообщения на сервер то выводит вот так
            else:
                sendmessage(id, f'Забанил {nick} на {time} по причине {reason}')
                writeLog(f'id:{id} имя:{pmessage(id)} забанил {nick} на {time} за {reason}')
        else:
            sendmessage(id, 'Команда "бан" введена неправильно. Возможно не написана причина? '
                            'Правильное написание команды: бан {игрок} {время} {причина} для временного бана, '
                            'и бан {игрок} {причина} для перманентного бана')  # ну если чето напутали вот так кароче
    else:
        sendmessage(id, 'Ты не админ!')
        writeLog(f'id:{id} имя:{pmessage(id)} попытался кого-то забанить: {message}')

def permabanplayer(message, id):
    if id in adminsid:  # если айди не в массиве айди админом
        nick = message.split(" ")[1]  # записывает ник
        r = message.split(" ")[2:20]  # разделяет причину от других слов в сообщении
        reason = ' '.join(r)  # записаывает причину
        com = rcon.command(f"tempban {nick} {reason}")  # и банит по двум параметрам
        if 'Ошибка' in com:
                sendmessage(id, f'Произошла ошибка при бане игрока {nick}. Игрок существует? Команда написана '
                            f'правильно?')  # и если ошибка при вводе сообщения на сервер то выводит вот так
        else:
                sendmessage(id, f'Забанил {nick} перманентно по причине {reason}')
                writeLog(f'id:{id} имя:{pmessage(id)} забанил {nick} перманентно')
    else:
        writeLog(f'id:{id} имя:{pmessage(id)} попытался кого-то забанить: {message}')
        sendmessage(id, 'Ты не админ!')


def randhumoreska(id):
    posts = my_t.method('wall.get', {'owner_id': -92876084, 'offset': 0, 'count': 100})["items"]  # берем посты из паблика юморески на каждый день
    posts_strings = [post['text'] for post in posts]  # засовываем их в переменную
    rand = random.randint(0, 50)  # берём рандомное число
    humoreska = posts_strings[rand]  # засовываем рандомный пост в переменную
    if len(humoreska) == 0:  # если юмореска пустая (а так бывает, например картинка без текста)
        writeLog(f'id:{id} имя:{pmessage(id)} посмотрел юмореску')
        sendmessage(id, posts_strings[rand + 1])  # то выдаём следующую по списку
    else:
        writeLog(f'id:{id} имя:{pmessage(id)} посмотрел юмореску')
        sendmessage(id, humoreska)  # иначе - отправляем юмореску пользователю

def getPlayers(id):
    com = rcon.command("list")  # отправляем на сервер команду /list
    com1 = com.split(" ")[10:25]
    com2 = ' '.join(com1)
    status = server.status()  # пробуем узнать статус сервера
    com2 = com2.replace('[0m', '')# убираем из полученого результата ненужные символы
    if status.players.online > 0:
        writeLog(f'id:{id} имя:{pmessage(id)} узнал онлайн сервера')
        sendmessage(id, f'Сейчас на сервере {status.players.online} игрока(ов): {com2}')  # пишем пользователю это
    else:
        writeLog(f'id:{id} имя:{pmessage(id)} узнал онлайн сервера')
        sendmessage(id, 'На сервере сейчас 0 человек :(')

def getPing(id):
    try:
        latency = server.ping()  # пробуем пингануть сервер
        status = server.status()  # пробуем узнать статус сервера
    except Exception as e:  # если вылезла ошибка
        sendmessage(id,
                    f'Сервер не отвечает по причине {e}. Свяжитесь с админом как можно скорее.')  # отправляем пользователю это сообщение
        writeLog(f'ОШИБКА ПОДКЛЮЧЕНИЯ: При проверке пинга сервера бот не смог подключиться к серверу')
        pass  # продолжаем работу скрипта
    else:  # если нет ошибок
        writeLog(f'id:{id} имя:{pmessage(id)} узнал пинг сервера')
        sendmessage(id,
                    f'Пинг: {latency} мс, на сервере сейчас {status.players.online} игрока(ов)')  # пишем это
        # вся эта хуйня показывает пинг сервера                   и кол-во игроков

def whitelistDef(id,message):
    if id in adminsid:  # проверяем является ли айди написавшего - вашим
        args = message.split(" ")
        if len(args) == 3:
            com1 = rcon.command("whitelist list")
            nick = args[2]
            if args[1] == 'добавить':  # проверяем что ВТОРОЕ СЛОВО - 'добавить'
                if nick in com1:
                    sendmessage(id, f'Игрок {nick} уже в вайтлисте!')
                else:
                    com = rcon.command(
                    f"whitelist add {nick}")  # отправляем ркон команду на добавление вайтлиста с третьим словом в сообщении пользователя
                    sendmessage(id, f'Добавил {nick} в вайтлист')  # сообщаем что всё хорошо
                    writeLog(f'vk.com/id{id} добавил {nick} в вайтлист')
            elif args[1] == 'удалить':  # если же ВТОРОЕ СЛОВО - удалить
                if {nick} in com1:
                    sendmessage(id, f'Удалил {nick} из вайтлиста')  # сообщаем что всё хорошо
                    com = rcon.command(
                        f"whitelist remove {nick}")  # отправляем ркон команду на удаление из вайтлиста с третьим словом в сообщении пользователя
                    writeLog(f'id:{id} имя:{pmessage(id)} удалил {nick} из вайтлиста')
                else:
                    sendmessage(id, f'Не удалось удалить {nick} из вайтлиста. Его там и не было!')
                    writeLog(f'id:{id} имя:{pmessage(id)} попытался удалить {nick} из вайтлиста, но его там не было')
        else:
            sendmessage(id,
                        'Нужно написать команду вида "Вайтлист {добавить/удалить} {никнейм}"')  # если написали "вайтлист" но другие слова неправильные, то выведт это сообщение
            writeLog(f'id:{id} имя:{pmessage(id)} неправильно написал команду вайтлиста')
    else:
        sendmessage(id, 'Ты не админ')
        writeLog(f'id:{id} имя:{pmessage(id)} попытался что-то сделать с вайтлистом: {message}')

def rusruletka(id):
    read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item()
    try:
        nick = read_dictionary[str(id)]
    except KeyError:
        sendmessage(id, 'Автор этого говнобота не смог осилить чтение данных из словаря. '
                        'Для тебя русская рулетка ПОКА ЧТО не работает, извини.')
        sendmessage(myvkid,f'Для @id{id} не сработала русская рулетка')
        writeLog(f'Для id:{id} имя:{pmessage(id)} не сработала русская  рулетка')
        pass
    rand = random.randint(0,6)
    bans = rcon.command('banlist').replace('Szarkan','')
    if nick in bans:
        sendmessage(id, 'Ты уже умер! Приходи через час!')
    else:
        if rand == 4:
            com = rcon.command(f'tempban {nick} 6h Проиграл в русскую рулетку')
            sendmessage(id, 'О нет! Ты проиграл :(')
            sendmessage(myvkid, f'@id{id} умер в русской рулетке под ником {nick}')
            writeLog(f'id:{id} имя:{pmessage(id)} умер в русской рулетке под именем {nick}')
        else:
            sendmessage(id, 'В этот раз тебе повезло...')
            writeLog(f'id:{id} имя:{pmessage(id)} выйграл в русской рулетке')

def addPlayerToList(id,idp,nick):
    read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item()
    read_dictionary[nick] = idp
    read_dictionary[idp] = nick
    sendmessage(id, f'Добавил в словарик @id{idp} под ником {nick}!')
    np.save('playersdict.npy', read_dictionary)
    read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item()
    writeLog(f'id:{id} имя:{pmessage(id)} добавил в словарик айди {idp} под ником {nick}')
    print(read_dictionary)

def getPlayerFromList(nick):
    nick = str(nick)
    read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item()
    try:
        b = read_dictionary[nick]
    except KeyError:
        sendmessage(id, 'Такого игрока нет, правильно ввёл ник или айди?')
        pass
    else:
        if nick.isdigit():
            sendmessage(id,f'@id{nick} это {b}')
        else:
            sendmessage(id, f'{nick} это @id{b}')
    writeLog(f'id:{id} имя:{pmessage(id)} узнал айди вк игрока {nick}')

# слушаем сообщения
try:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            # Чтобы наш бот не слышал и не отвечал на самого себя
            if event.to_me:
                # Для того чтобы бот читал все с маленьких букв
                message = event.text
                args = message.split(" ")
                # Получаем id пользователя
                id = event.user_id

                if args[0] in ping:  # если в сообщении которое отправил челикс ПЕРВОЕ слово это одно из массива ping
                    getPing(id)
                elif args[0] in players:  # если в сообщении которое отправил челикс ПЕРВОЕ слово это одно из массива players
                    getPlayers(id)
                elif args[0] in whitelist:  # если ПЕРВОЕ СЛОВО это одно из списка 'whitelist', то
                    whitelistDef(id,message)
                elif args[0] in ban:  # если введеное сообщение содержит в себе слово из массива бан
                    banplayer(message, id)  # выполняем функцЫю, она сверху
                elif args[0] in permaban:
                    permabanplayer(message, id)

                elif args[0] in ruletka:
                    rusruletka(id)

                elif args[0] == 'кто':
                    if id in adminsid:
                        getPlayerFromList(args[1])
                    else:
                        sendmessage(id, 'Ты не админ!')
                elif args[0] == 'добигрока':
                    if id in adminsid:
                        addPlayerToList(id ,args[1], args[2])
                    else:
                        sendmessage(id, 'Ты не админ!')
                elif args[0] == 'айди':
                    if id in adminsid:
                        idt = str(args[1]).replace('https://vk.com/','')
                        sendmessage(id, f'{getId(idt)}')
                    else:
                        sendmessage(id, 'Ты не админ!')

                elif args[0] in unban:  # если из массива анбан
                    if id in adminsid:  # если айди в списке айди админом
                        nick = args[1]  # берём ник за переменную, зачем не знаю ахахаахха
                        com = rcon.command(f"pardon {nick}")
                        if 'Ошибка' in com:  # если в выводе команды ошибка, то пишем это написавшему
                            sendmessage(id,
                                        f'Произошла ошибка при разбане игрока {nick}. Игрок существует? Команда написана '
                                        f'правильно?')
                        else:
                            sendmessage(id, f'Разбанил игрока {nick}')  # ну а если нет то разбаниваем
                            writeLog(f'id:{id} имя:{pmessage(id)} разбанил игрока {nick}')
                    else:
                        sendmessage(id, 'Ты не админ!')
                        writeLog(f'id:{id} имя:{pmessage(id)} попытался разбанить кого-то: {message}')

                elif args[0] in kick:  # ну тут кикает кароче, принимает либо 3 значения, либо 2
                    if id in adminsid:
                        if len(args) > 2:
                            nick = args[1]
                            r = args[3:]
                            reason = ' '.join(r)  # записаывает причину
                            com = rcon.command(f'kick {nick} {reason}')
                            if 'Invalid name or UUID' in com:  # проверяет есть ли ошибка в нике
                                sendmessage(id, f'Не удалось кикнуть. Такого игрока нет, либо ник написан неправильно')
                                writeLog(f'id:{id} имя:{pmessage(id)} не смог кикнуть {nick}')
                            else:
                                sendmessage(id,
                                                f'Кикнул {args[1]} по причине {reason}')
                                writeLog(f'id:{id} имя:{pmessage(id)} кикнул {nick} с причиной {reason}')
                        elif len(args) == 2:
                            com = rcon.command(f'kick {nick}')
                            if 'Invalid name or UUID' in com:  # проверяет есть ли ошибка в нике
                                sendmessage(id, f'Не удалось кикнуть. Такого игрока нет, либо ник написан неправильно')
                            else:
                                sendmessage(id, f'Кикнул {nick} без причины')
                                writeLog(f'id:{id} имя:{pmessage(id)} кикнул {nick} без причины')
                        else:  # ну и если слов не 3 и не 2 то выводит это
                            sendmessage(id, 'Не удалось кикнуть. Либо много аргументов, либо ну хз кароче иди нахуй')
                    else:
                        sendmessage(id, 'Ты не админ!')
                        writeLog(f'id:{id} имя:{pmessage(id)} попытался кого-то кикнуть')

                elif args[0] in tp:
                    if id in adminsid:

                        if len(args) == 5:
                            player = args[1]
                            x = args[2]  # ну кароче вкратце он в переменные кладёт определенные слова
                            y = args[3]  # тоесть написал ты боту "тп игрок 10 10 10", и он распределит
                            z = args[4]  # все эти значения, но только если не больше 5 слов в сообещнии
                            com = rcon.command(f'tp {player} {x} {y} {z}')
                            if 'No entity was found' in com:
                                sendmessage(id, f'Такого игрока нет на сервере!')
                                writeLog(f'id:{id} имя:{pmessage(id)} не смог телепортировать {player}')
                            else:
                                sendmessage(id,
                                        f'Телепортировал {player} на координаты x{x} y{y} z{z}')  # ну а здесь он тпает исходя из переменных
                                writeLog(f'id:{id} имя:{pmessage(id)} телепортировал {player} на координаты x{x} y{y} z{z}')
                        else:
                            sendmessage(id, 'Команда телепорта введена неправильно. Нужно: tp НИК X Y Z')
                    else:
                        sendmessage(id, 'Ты не админ!')

                elif args[0] == 'всем:':
                    if id in adminsid:
                        mes1 = ' '.join(args[1:])
                        com = rcon.command(
                            f'say {mes1}')  # просто шлёт всем сообщение через команду say, дефолт майнкрафт
                        sendmessage(id,
                                    f'Написал на сервер собщение: {message.replace("всем:", "")}')  # можно заменить /tellraw @a "{message.replace("всем:","")}", одна хуйня получится
                        writeLog(f'id:{id} имя:{pmessage(id)} написал на сервер {mes1}')
                    else:
                        sendmessage(id, 'Ты не админ!')

                elif args[0] in donate:  # выдать донат посредством LuckPerms
                    if id in adminsid and permissions == 0:
                        if len(args) == 4:
                            nick = args[1]
                            perm = args[2]
                            time = args[3]
                            com = rcon.command(
                                f'lp user {nick} parent addtemp {perm} {time}')
                            sendmessage(id, f'Выдал привелегию {perm} игроку {nick} '
                                            f'на {time}, вывод команды: {com}')
                            writeLog(f'id:{id} имя:{pmessage(id)} выдал привелегию {perm} игроку {nick} на {time}')
                        elif len(args) < 4:
                            sendmessage(id, 'Команда введена неправильно, отсутствуют '
                                            'параметры. Правильно: выдатьдонат '
                                            '{название привелегии} {игрок} {время}')
                        elif len(args) > 4:
                            sendmessage(id, 'Слишком много параметров! Правильно: выдатьдонат '
                                            '{название привелегии} {игрок} {время}')
                    elif id in adminsid and permissions == 1:
                        if len(args) == 3:
                            nick = args[1]
                            perm = args[2]
                            com = rcon.command(
                                f'pex user {nick} add {perm}')
                            sendmessage(id, f'Выдал привелегию {perm} игроку {nick} '
                                            f', вывод команды: {com}')
                        elif len(args) < 3:
                            sendmessage(id, 'Команда введена неправильно, отсутствуют '
                                            'параметры. Правильно: выдатьдонат {ник}'
                                            '{название привелегии}')
                        elif len(args) > 3:
                            sendmessage(id, 'Слишком много параметров! Правильно: выдатьдонат {ник}'
                                            '{название привелегии} ')
                    else:
                        sendmessage(id, 'Ты не админ!')
                elif message == 'выключись':
                    if id in adminsid:
                        sendmessage(id, 'Выключаюсь!')
                        writeLog(f'id:{id} имя:{pmessage(id)} выключил бота из ВК')
                        print('Бот выключен командой из ВК')
                        sys.exit(0)
                    else:
                        sendmessage(id, 'Ты не админ!')
                        writeLog(f'id:{id} имя:{pmessage(id)} попытался выключить бота')
                elif message == 'перезагрузись':
                    if id in adminsid:
                        sendmessage(id, 'Перезагружаюсь!')
                        writeLog(f'id:{id} имя:{pmessage(id)} перезагрузил бота')
                        os.system("python3 vkbot.py")
                        sys.exit(0)
                    else:
                        sendmessage(id, 'Ты не админ!')
                        writeLog(f'id:{id} имя:{pmessage(id)} попытался перезагрузить бота')

                # команды для обычных юзеров
                elif args[0] == 'донат':
                    sendmessage(id,f'Вы можете приобрести донат здесь: {donatelink}')
                    writeLog(f'id:{id} имя:{pmessage(id)} вызвал донат')
                elif args[0] == 'ком':  # отправить команду ркон если её нет в этом скрипте чреез слеш
                    rconcommand(message.replace("ком", ""), id)
                    writeLog(f'id:{id} имя:{pmessage(id)} написал команду на сервер')
                elif args[0] == 'пися':  # это просто ржака
                    sendmessage(id, 'попа')
                    writeLog(f'id:{id} имя:{pmessage(id)} пися')
                elif args[0] == 'юмореска':
                    randhumoreska(id)
                    writeLog(f'id:{id} имя:{pmessage(id)} вызвал юмореску')
                elif args[0] == 'пм':
                    if len(args) >= 3:
                        message1 = args[2:]
                        name = pmessage(id)
                        nick = message1[1]
                        mes = ' '.join(message1[2:len(message1)])
                        list = rcon.command('list')
                        players = ' '.join(list.split(" ")[10:25])
                        if nick in players.lower():
                            com = rcon.command(f'msg {nick} {name} написал вам: {mes}')
                            sendmessage(id, f'Отправил {nick} личное сообщение: {mes}. Вывод: {com}')
                            writeLog(f'id:{id} имя:{pmessage(id)} написал сообщение игроку {nick}: {mes}')
                        else:
                            com = rcon.command(f'mail send {nick} {name} написал вам: {mes}')
                            sendmessage(id, f'Отправил {nick} письмо: {mes} Вывод: {com}')
                            writeLog(f'id:{id} имя:{pmessage(id)} написал  сообщение игроку {nick}: {mes}')
                    else:
                        sendmessage(id, 'Неправильно ввёл! Правильно: пм {ник} {сообщение до 100 слов}')
                elif args[0] == 'анон':
                    if len(args) >= 3:
                        message1 = args[2:]
                        nick = args[1]
                        list = rcon.command('list')
                        mes = ' '.join(message1)
                        players = ' '.join(list.split(" ")[10:25])
                        if nick in players.lower():
                            com = rcon.command(f'msg {nick} Вам анонимное послание: {mes}')
                            sendmessage(id, f'Отправил {nick} анонимное письмо: {mes} Вывод: {com}')
                            writeLog(f'id:{id} имя:{pmessage(id)} написал анонимное сообщение игроку {nick}: {mes}')
                        else:
                            com = rcon.command(f'mail send {nick} Вам анонимное послание: {mes}')
                            sendmessage(id, f'Отправил {nick} анонимное письмо: {mes} Вывод: {com}')
                            writeLog(f'id:{id} имя:{pmessage(id)} написал анонимное сообщение игроку {nick}: {mes}')
                    else:
                        sendmessage(id, 'Неправильно ввёл! Правильно: анон {ник} {сообщение до 100 слов}')
                        writeLog(f'id:{id} имя:{pmessage(id)} неправильно ввёл команду анонимного сообщения')

                else:  # если ничего из этого списка не было написано - пишет вот это
                    sendmessage(id, f'Неизвестная команда. Если у вас есть вопрос, то пишите админу @szarkan')
                    writeLog(f'id:{id} имя:{pmessage(id)} написал что-то непонятное: {message}')
except Exception as error:  # если чота случилось с вк апи
    try:
        sendmessage(myvkid, f'Я лёг по причине {error}')  # пытаемся отправить сообщение с ошибкой
        sendmessage(myvkid, 'Пробуем перезапуститься...')
        writeLog(f'ОШИБКА: бот лёг по причине {error}')
        pass
    except Exception as e:
        print(f'Не смог отправить сообщение в вк. Причина: {e}')  # а если даже сообщение не отправляется, то пишем ошибку в консоль
        writeLog(f'ОШИБКА: бот не смог отправить сообщение в ВК и лёг по причине {error}')
        pass
    sleep(15)
    writeLog('Пробуем перезапуститься')
    os.system("python3 vkbot.py")
    sys.exit(0)

# код карчое являестя собственостью серёжи юдина vk.com/szarkan, не воруйте пожалуйста !!!
# dotmix пидорас кстати
