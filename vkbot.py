import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from mctools import RCONClient, errors
from mcstatus import MinecraftServer
from slovarik_minecraft import *
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
longpollb = VkBotLongPoll(group_t, '210306238')
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

print(now)
if '23-07-2022' in now or '22-07-2022' in now:
    sendmessage(myvkid, 'Оплати мой хостинг!!!!')

def sendmessageLink(id, text): # ээ хуй знает зачем я это добавил, но как я вижу он просто отправляет ссылку ВК
    if id.isdigit():
        group_t.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})
    else:
        id = id.replace('https://vk.com/','').replace('vk.com/','')
        id = getId(id)
        group_t.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})

def pmessage(id): # тут узнавать имя фамилию по айди
    user = group_t.method("users.get", {"user_ids": id})
    fullname = user[0]['first_name'] + ' ' + user[0]['last_name']
    return fullname

def getId(str): # ну тут кароче узнавать айди ВК по короткому именем
    print(str)
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
        try_count += 1 # он попытается запустить этот адский скрипт ещё три раза
        sleep(5)
    else:
        sendmessage(myvkid, f'К РКОНу подключился! Сервер отвечает на запросы с задержкой {server.ping()}мс. '
                            f'Бот успешно запущен!')
        writeLog('Подключился к серверу')
        break
else: # с трёх раз не завёлся - вырубаемся нах, и включаем режим ожидания
    sendmessage(myvkid, f'Три попытки переподключиться к серверу оказались безуспешными. Выключаюсь.')
    writeLog('Выключаюсь из-за неудачного запуска')
    os.system("python3 waiting.py")
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
        com = rcon.command(f"ban {nick} {reason}")  # и банит по двум параметрам
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
    try:
        latency = round(server.ping(),2)  # пробуем пингануть сервер
        status = server.status()  # пробуем узнать статус сервера
        com = rcon.command("list")  # отправляем на сервер команду /list
    except Exception as e:  # если вылезла ошибка
        sendmessage(id,
                    f'Сервер не отвечает по причине {repr(e)}. Хз чо с ним ахаххахах')  # отправляем пользователю это сообщение
        writeLog(f'ОШИБКА ПОДКЛЮЧЕНИЯ: При проверке пинга сервера бот не смог подключиться к серверу')
        pass  # продолжаем работу скрипта
    else:  # если нет ошибок
        com1 = ' '.join(com.split(" ")[10:25])
        com1 = com1.replace('[0m', '')# убираем из полученого результата ненужные символы
        if status.players.online > 0:
            writeLog(f'id:{id} имя:{pmessage(id)} узнал онлайн сервера')
            sendmessage(id, f'Пинг сервера: {latency}мс, ТПС: 20. \n\nСейчас на сервере {status.players.online} игрока(ов): {com1}')  # пишем пользователю это
        else:
            writeLog(f'id:{id} имя:{pmessage(id)} узнал онлайн сервера')
            sendmessage(id, f'Пинг сервера: {latency}мс, ТПС: 20. \n\nНа сервере сейчас 0 человек :(')

def whitelistDef(id,args):
    if id in adminsid:  # проверяем является ли айди написавшего - вашим
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
                if nick in com1:
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
        writeLog(f'id:{id} имя:{pmessage(id)} попытался что-то сделать с вайтлистом: {args}')

def rusruletka(id):
    read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item()
    if str(id) not in read_dictionary.values():
        sendmessage(id, 'Ты не игрок сервера.')
    else:
        try:
            nick = read_dictionary[str(id)] # пробуем достать ник игрока через его айди Вк из словаря
        except KeyError:
            sendmessage(id, 'Эээ... Либо словарь шалит, либо тебя нет в списке игроков!') # не получилось - пишем ему об этом, и логируем
            sendmessage(myvkid,f'Для @id{id} не сработала русская рулетка')
            writeLog(f'Для id:{id} имя:{pmessage(id)}   не сработала русская  рулетка')
            pass
        rand = random.randint(0,6) # делаем рандомное число, как в револьвере - 6
        bans = rcon.command('banlist').replace(gameNick,'') # в команде /banlist есть ваш ник, поэтмоу убираем его от туда, чтобы и вы смогли поиграть в русскую рулетку
        if nick in bans:
            sendmessage(id, 'Ты уже умер! Приходи через час!') # если чувачок уже забанен - пишем ему
        else:
            if rand == 4: # а иначе на там кароче всё как часы работает идите нахуй
                com = rcon.command(f'tempban {nick} 6h Проиграл в русскую рулетку')
                sendmessage(id, 'О нет! Ты проиграл :(')
                sendmessage(myvkid, f'@id{id} умер в русской рулетке под ником {nick}')
                writeLog(f'id:{id} имя:{pmessage(id)} умер в русской рулетке под именем {nick}')
            else:
                sendmessage(id, 'В этот раз тебе повезло...')
                writeLog(f'id:{id} имя:{pmessage(id)} выйграл в русской рулетке')

def addPlayerToList(id,idp,nick):
    read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item() # загружаем словарь
    read_dictionary[nick] = idp # добавляем айди вк игрока по нику
    read_dictionary[idp] = nick # тоже самое наоборот
    sendmessage(id, f'Добавил в словарик @id{idp} под ником {nick}!')
    np.save('playersdict.npy', read_dictionary) # сохраняем словарь
    read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item() # зачем-то загружаем его заново ахахах
    writeLog(f'id:{id} имя:{pmessage(id)} добавил в словарик айди {idp} под ником {nick}')

def addPlayerToListStr(id,idp,nick):
    read_dict = np.load('streamers.npy', allow_pickle='TRUE').item() # та же хуйня что и сверху, но добавляет игрока в список стримеров
    read_dict[nick] = idp
    read_dict[idp] = nick
    sendmessage(id, f'Добавил в словарик стримеров @id{idp} под ником {nick}!')
    np.save('streamers.npy', read_dict)
    read_dic = np.load('streamers.npy', allow_pickle='TRUE').item()
    writeLog(f'id:{id} имя:{pmessage(id)} добавил в словарик стримеров айди {idp} под ником {nick}')
    print(read_dictionary)

def deletePlayerFromListStr(arg): # удаление из списка стрмиеров
    read_dict = np.load('streamers.npy', allow_pickle='TRUE').item()
    arg1 = read_dict[arg] # берем значение айди игрока
    arg2 = read_dict[arg1] #  берем значение ника игрока
    read_dict.pop(arg1) #  и удаляем нахуй его
    read_dict.pop(arg2)
    print(read_dict) # выводим зачем-то
    np.save('streamers.npy', read_dict) #  сохраняем

def getPlayerFromList(nick):
    nick = str(nick)
    if 'vk.com/' in nick: # убираем ссылку из ссылки
        nick = str(getId(nick.replace('vk.com/','').replace('https://','')))
    read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item()
    try:
        b = read_dictionary[nick] # пытаемся найти значение
    except KeyError:
        sendmessage(id, 'Такого игрока нет, правильно ввёл ник или айди?') # не нашли - шлём наухй
        pass
    else:
        if nick.isdigit(): # проверяем является ли значение цифрами (тобишь айди вк)
            sendmessage(id,f'@id{nick} это {b}')
        else:
            sendmessage(id, f'{nick} это @id{b}')
    writeLog(f'id:{id} имя:{pmessage(id)} узнал айди вк игрока {nick}')

def deletePlayerFromList(arg): # удаление из списка игроков
    read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item()
    arg1 = read_dictionary[arg]
    arg2 = read_dictionary[arg1]
    read_dictionary.pop(arg1)
    read_dictionary.pop(arg2)
    print(read_dictionary)
    np.save('playersdict.npy', read_dictionary)


def application(id,message):
    if len(message) == 1: # если челикс просто написал "заявка" - выводим текст заявки
        sendmessage(id, applicationMessage)
    elif len(message) > 3: # иначе - обрабатываем
        zay = ' '.join(message)
        zay = '\n ' + zay + '\n '
        newApp = '='*20 + '\n' + f'Пришла новая заявка от @id{id}! \n{zay}' + '\n' + '='*20
        sendmessage(myvkid, newApp)
        sendmessage(myvkid, f'принять {id} {message[2]}')
        sendmessage(myvkid, f'принять {id} {message[3]}')
        sendmessage(myvkid, f'отклонить {id}')
        sendmessage(id,'Переслал твою заявку! Ожидай решения администрации :)') # ну там краоче иди нахуй много объяснять
    elif 3 > len(message) > 1:
        sendmessage(id, 'Чего-то не хватает... Видимо твоя заявка слишком короткая, попробуй ещё раз.')

def accept(id,nick):
    sendmessage(id,'Твоя заявка одобрена! Теперь ты можешь зайти на наш прекрасный сервер!\n' \
                '\n'
                f'Твой ник: {nick}\n' \
                'IP: 45.93.200.49:25578\n' \
                'Версия: 1.19\n' \
                'Если есть вопросы - обращайся @szarkan :)\n' \
                'Наша беседа: https://vk.me/join/OKMN2Ypd3LMSaZa5t5kxAOGCbuwThZ/t7MA=\n' \
                'Вход в беседу обязателен, там новости, анонсы да и пообщаться можно')
    sendmessage(id,'У этого бота есть функционал, можешь узнать его команды написав ему "команды"\n'
                   'Либо поспрашивать его простенькие вопросы :)')
    com = rcon.command(f'whitelist add {nick}')
    sendmessage(myvkid, f'Добавил @id{id} в вайтлист с ником {nick}!')
    sendmessage(myvkid, f'Вывод команды: {com}')
    addPlayerToList(myvkid,id,nick)
    writeLog(f'Принял заявку от {pmessage(id)}, ник: {nick}')

def decline(idd, message=''):
    if len(message) == 0:
        sendmessage(idd, deniedMessage)
    else:
        mes = deniedMessageWithReason + message
        sendmessage(idd, mes)
    writeLog(f'Отклонил заявку от {id}')

# слушаем сообщения
try:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            message = event.text
            args = message.split(" ")
            # Получаем id пользователя
            id = event.user_id

            messageOther = message.replace('\n',' \n ') # это другая строка, у которой \n заменяется на тоже самое, но с пробелами
            message = message.lower()
            args2 = messageOther.split(" ") # и из этой строки мы делаем массив

            print(f'args{args}',f'args2{args2}',f'messageOther: {messageOther}',f'message: {message}')
            if args[0] in players:  # если в сообщении которое отправил челикс ПЕРВОЕ слово это одно из массива ping
                getPlayers(id)



            elif args[0] in whitelist:  # если ПЕРВОЕ СЛОВО это одно из списка 'whitelist', то
                whitelistDef(id,args)
            elif args[0] in ban:  # если введеное сообщение содержит в себе слово из массива бан
                banplayer(message, id)  # выполняем функцЫю, она сверху
            elif args[0] in permaban:
                permabanplayer(message, id)
            elif args2[0] in applicationWord:
                application(id,args2)
            elif '1.' in message and '2.' in message:
                sendmessage(id, 'Не уверен, но помоему ты только что написал мне заявку. Если так - ты написал её '
                                'без слова "заявка" в первой строке!')
            elif args[0] == 'Принять' or args[0] == 'принять':
                if id in adminsid:
                    accept(args[1],args[2])
                else:
                    sendmessage(id, 'Ага, мож тебе ещё хуй отсосать?')

            elif args[0] == 'Отклонить' or args[0] == 'отклонить':
                if id in adminsid:
                    if len(args) == 2:
                        decline(args[1])
                    elif len(args) > 2:
                        decline(args[1],' '.join(args[2:]))
                    else:
                        sendmessage(id, 'чота ты еблан')
                else:
                    sendmessage(id, 'Ага, мож тебе ещё хуй отсосать?')

            elif args[0] in ruletka:
                rusruletka(id)

            elif args[0] == 'кто':
                read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item()
                if str(id) in read_dictionary:
                    nn = ''
                    if len(args) < 2:
                        sendmessage(id, 'Ты не ввёл ссылку или ник!!!!!!!!!!!')
                    else:
                        if '@' in args[1]:
                            for i in range(3,len(args[1])):
                                if args[1][i] != '|':
                                    nn += args[1][i]
                                else:
                                    print(nn)
                                    getPlayerFromList(nn)
                        elif 'catcraftmc' in message:
                            sendmessage(id, 'Это же я!')
                        else:
                            getPlayerFromList(args[1])
                            writeLog(f'id:{id} имя:{pmessage(id)} узнал ник или айди {args[1]}')
                else:
                    sendmessage(id, 'Команда доступна только игрокам сервера')

            elif args[0] == 'добигрока':
                if id in adminsid:
                    addPlayerToList(id ,args[1], args[2])
                else:
                    sendmessage(id, 'Ты не админ!')

            elif args[0] == 'добигрокас':
                if id in adminsid:
                    addPlayerToListStr(id ,args[1], args[2])
                else:
                    sendmessage(id, 'Ты не админ!')

            elif args[0] == 'удалить':
                if id in adminsid:
                    if len(args) < 2:
                        sendmessage(id,'Аргументов не хватает')
                    else:
                        try:
                            deletePlayerFromList(args[1])
                        except Exception as e:
                            sendmessage(id, f'Неа, не получилось: {e}')
                        else:
                            sendmessage(id, f'Удалил значение {args[1]} из словаря')
                else:
                    sendmessage(id, 'ты не админнннннщвфыаждлывфывдвыджэ')

            elif args[0] == 'удалитьс':
                if id in adminsid:
                    if len(args) < 2:
                        sendmessage(id,'Аргументов не хватает')
                    else:
                        try:
                            deletePlayerFromListStr(args[1])
                        except Exception as e:
                            sendmessage(id, f'Неа, не получилось: {e}')
                        else:
                            sendmessage(id, f'Удалил значение {args[1]} из словаря')
                else:
                    sendmessage(id, 'ты не админнннннщвфыаждлывфывдвыджэ')

            elif args[0] == 'айди':
                if id in adminsid:
                    if len(args) < 2:
                        sendmessage(id, 'Аргументов нехватает, дебил!')
                    else:
                        if 'vk.com/' in str(args):
                            idt = str(args[1]).replace('vk.com/','').replace('https://','')
                            sendmessage(id, f'{getId(idt)}')
                else:
                    sendmessage(id, 'Ты не админ!')

            elif args[0] == 'словарь':
                if id in adminsid:
                    read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item()
                    sl = ''
                    num = 0
                    for key in read_dictionary.keys():
                        if read_dictionary[key].isdigit():
                            pass
                        else:
                            num += 1
                            sl += f'{num}. {read_dictionary[key]} \n'
                    sendmessage(id, sl)
                else:
                    sendmessage(id,'Ты не админ!')

            elif args[0] == 'словарь2':
                if id in adminsid:
                    num = 0
                    read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item()
                    sl = ''
                    for key in read_dictionary.keys():
                        if read_dictionary[key].isdigit():
                            num += 1
                            sl += f'{num}. @id{read_dictionary[key]} \n'
                        else:
                            pass
                    sendmessage(id, sl)
                else:
                    sendmessage(id,'Ты не админ!')

            elif args[0] == 'напиши':
                if id in adminsid:
                    sendmessageLink(args[1],' '.join(args[2:]))
                else:
                    sendmessage(id, 'ди нах')

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


            elif args[0] == 'яснимаю':
                read_streamers = np.load('streamers.npy', allow_pickle='TRUE').item()
                if str(id) in read_streamers:
                    read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item()
                    nick = read_dictionary[str(id)]
                    com = rcon.command(f'lp user {nick} meta addprefix 1000 "&4◎ "')
                    com1 = rcon.command(f'say {nick} §4начал запись! Использование бан-вордов грозит 7 дневным мутом!')
                    sendmessage(id,'Выдал префикс, игроки предупреждены об использовании банвордов!')
                else:
                    sendmessage(id, 'Ты не контентмейкер! Если хочешь таковым стать - пиши @szarkan')

            elif args[0] == 'янеснимаю':
                read_streamers = np.load('streamers.npy', allow_pickle='TRUE').item()
                if str(id) in read_streamers:
                    read_dictionary = np.load('playersdict.npy', allow_pickle='TRUE').item()
                    nick = read_dictionary[str(id)]
                    com = rcon.command(f'lp user {nick} meta clear')
                    com1 = rcon.command(f'say {nick} §4перестал записывать. Можете писать чо хотите!')
                    sendmessage(id, 'Префикс снял.')
                else:
                    sendmessage(id, 'Ты не контентмейкер! Если хочешь таковым стать - пиши @szarkan')

            elif args[0] in kick:  # ну тут кикает кароче, принимает либо 3 значения, либо 2
                if id in adminsid:
                    if len(args) > 2:
                        nick = args[1]
                        reason = ' '.join(args[3:])
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

            elif args[0] == 'всем:' or args[0] == 'всем':
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
                else:
                    sendmessage(id, 'Ты не админ!')
            elif message == 'выключись':
                if id in adminsid:
                    sendmessage(id, 'Выключаюсь!')
                    writeLog(f'id:{id} имя:{pmessage(id)} выключил бота из ВК')
                    print('Бот выключен командой из ВК')
                    os.system("python3 waiting.py")
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
            elif args[0] == 'ком':  # отправить команду ркон если её нет в этом скрипте чреез слеш
                if id in adminsid:
                    rconcommand(message.replace("ком", ""), id)
                    writeLog(f'id:{id} имя:{pmessage(id)} написал команду на сервер')
                else:
                    sendmessage(id, 'Ты не админ!')
            elif args[0] == 'партнерка':
                if id in adminsid:
                    idd = str(read_dictionary[args[1]])
                    sendmessage(idd, 'Спасибо что привёл друга! Теперь тебе доступен набор /kit opros (он одноразовый)')
                    com = rcon.command(f'lp user {args[1]} permission set essentials.kits.friend true')
                    sendmessage(id, f'Ага, для {args[0]}, вывод: {com}')
            # команды для обычных юзеров
            elif args[0] == 'донат':
                sendmessage(id,f'Вы можете приобрести донат здесь: {donatelink}')
                writeLog(f'id:{id} имя:{pmessage(id)} вызвал донат')
            elif args[0] == 'пися':  # это просто ржака
                sendmessage(id, 'попа')
                writeLog(f'id:{id} имя:{pmessage(id)} пися')
            elif args[0] == 'попа':
                sendmessage(id, 'пися')
                writeLog(f'id:{id} имя:{pmessage(id)} попа')
            elif args[0] in helpcoms:
                sendmessage(id, helpMes)
            elif args[0] == 'юмореска':
                sendmessage(id,'Пока что не работают :(')
               # randhumoreska(id)
               # writeLog(f'id:{id} имя:{pmessage(id)} вызвал юмореску')
            elif args[0] == 'пм':
                if str(id) in read_dictionary.values():
                    if len(args) >= 3:
                        name = pmessage(id)
                        nick = args[1]
                        mes = ' '.join(args[2:])
                        list = rcon.command('list')
                        players = ' '.join(list.split(" ")[10:25])
                        if nick.lower() in players.lower():
                            com = rcon.command(f'msg {nick} {name} написал вам: {mes}')
                            sendmessage(id, f'Отправил {nick} личное сообщение: {mes}. Вывод: {com}')
                            writeLog(f'id:{id} имя:{pmessage(id)} написал сообщение игроку {nick}: {mes}')
                        else:
                            com = rcon.command(f'mail send {nick} {name} написал вам: {mes}')
                            sendmessage(id, f'Отправил {nick} письмо: {mes} Вывод: {com}')
                            writeLog(f'id:{id} имя:{pmessage(id)} написал  сообщение игроку {nick}: {mes}')
                    else:
                        sendmessage(id, 'Неправильно ввёл! Правильно: пм {ник} {сообщение до 100 слов}')
                        writeLog(f'id:{id} имя:{pmessage(id)} не смог написать ПМ: {args}')
                else:
                    sendmessage(id, 'Ты не игрок нашего сервера, либо не находишься в списке!')
            elif args[0] == 'анон':
                if str(id) in read_dictionary.values():
                    if len(args) >= 3:
                        nick = args[1]
                        list = rcon.command('list')
                        mes = ' '.join(args[2:])
                        players = ' '.join(list.split(" ")[10:25])
                        if nick.lower() in players.lower():
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
                else:
                    sendmessage(id, 'Ты не игрок нашего сервера, либо тебя нет в списке!')
                    
            # это кароче имитация жизни бота воот
            elif 'пасиб' in message or 'спс' in message or 'thx' in message:
                sendmessage(id, 'Не за что! ^_^')
            elif 'ты кто' in message or 'кто ты' in message:
                sendmessage(id, 'Я - многофункциональный бот, созданный, чтобы облегчить жизнь бедному админу.\n'
                                'У меня НЕТ самосознания, я всего лишь строчки кода :)\n'
                                'Можешь узнать что я могу, написав мне "команды"')
            elif 'идея' in message or 'идею' in message:
                sendmessage(id, 'Увы, я просто бот, но свои идеи ты можешь предложить моему создателю!\n'
                                'Я слышал за хорошие идеи он выдаёт плюшки :)\n'
                                f'Пиши ему: @id{myvkid}')
            elif 'вопрос' in message:
                sendmessage(id, f'По вопросикам лучше обращайся напрямую к админу: @id{myvkid}')
            elif 'ахват мир' in message:
                sendmessage(id, 'Не знаю точно, что ты имел ввиду, но захватывать мир я не собираюсь. Пока что.')
            elif 'как дела' in message:
                sendmessage(id, 'Да потихонечку, сижу вот, заявочки обрабатываю...')
            elif 'ты пидорас' in message:
                sendmessage(id, 'От пидораса слышу')
            elif 'айпи' in message or 'ip' in message:
                sendmessage(id, f'Нна {serverip}:{serverport}, не теряй больше')
            elif 'https://vk.com/' in args[0] or 'vk.com/' in args[0]:
                sendmessage(id, 'Что это за ссылка? Если хочешь узнать ник, то введи команду "кто {ссылка вк}"')
            elif message == 'бот':
                sendmessage(id, 'Что?')
            elif args[0] == '':
                sendmessage(id, 'Я не могу смотреть на стикеры, фото или видео!!! Я слепой!!!')
            elif 'нормально общайся' in message:
                sendmessage(id, 'че борзый самый нахуй?')
            elif 'привет' in message or 'хай' in message:
                sendmessage(id, 'Привет! Хочешь оставить заявочку на сервер? Или узнать мои команды? Их можно узнать'
                                'командой "команды"!')
            elif 'еблан' in message:
                sendmessage(id, 'Я тебе кибер рукой пизды дам и айпи твой задудошу гандон')
            elif 'иди нахуй' in message or 'нахуй иди' in message:
                sendmessage(id, 'сам пошёл нахуй!!! пидор')
            elif 'соси' in args2:
                sendmessage(id, 'Сосать твоя забота, гандон!! ')
            elif 'ок' in args2 or message == 'жду' or 'ура' in message:
                sendmessage(id,'^_^')
            elif 'вайтлист' in message:
                sendmessage(id, 'Чтобы попасть в вайтлист нашего замечательного сервера введи команду "заявка"')
            elif message == 'бля':
                sendmessage(id, 'Не ругайся!')
            elif 'имитация жизни' in message:
                sendmessage(id,'Нихуя тут гений нашёлся, а ты типа не имитации жизни? Амёба бля')



            else:  # если ничего из этого списка не было написано - пишет вот это
                sendmessage(id, unknowCom)
                try:
                    writeLog(f'id:{id} имя:{pmessage(id)} написал что-то непонятное: {message}')
                except Exception as e:
                    writeLog(f'id:{id} имя:{pmessage(id)} написал что-то вообще непонятное и вызвал ошибку: {e}')
                    pass

except Exception as error:  # если чота случилось с вк апи
    try:
        sendmessage(myvkid, f'Я лёг по причине {repr(error)}')  # пытаемся отправить сообщение с ошибкой
        sendmessage(myvkid, 'Пробуем перезапуститься...')
        writeLog(f'ОШИБКА: бот лёг по причине {repr(error)}')
        pass
    except Exception as e:
        print(f'Не смог отправить сообщение в вк. Причина: {repr(e)}')  # а если даже сообщение не отправляется, то пишем ошибку в консоль
        writeLog(f'ОШИБКА: бот не смог отправить сообщение в ВК и лёг по причине {error}')
        pass
    sleep(5)
    writeLog('Пробуем перезапуститься')
    os.system("python3 vkbot.py")
    sys.exit(0)
# код карчое являестя собственостью серёжи юдина vk.com/szarkan, не воруйте пожалуйста !!!
# dotmix пидорас кстати
