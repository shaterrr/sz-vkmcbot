import numpy as np # ЗАПУСТИТЕ ЭТОТ ФАЙЛ И ПОСЛЕ ЭТОГО УДАЛИТЕ ЭТУ СТРОЧКУ И ЕЩЁ СНИЗУ ОДНУ

# это слова которые можно использовать для каждой команды, можете добавить свои или убрать лишние
ping = ('пинг', 'ping', 'gbyu', 'тпс')
players = ('игроки', 'buhjrb', 'online', 'players', 'онлайн')
ban = ('бан', 'забанить', 'ban', 'tempban', ',fy', 'pf,fybnm', 'ифт', 'пермач', 'пермбан', 'permban', 'gthvfx',
       'зукьифт')
permaban = ('пермач', 'пермабан','permaban')
unban = ('разбан', 'разбанить', 'hfp,fy', 'hfp,fybnm', 'unban', 'pardon', 'гтифт')
whitelist = ('вайтлист', 'вл', 'wl', 'whitelist', 'dfqnkbcn', 'dk')
kick = ('кик', 'кикнуть', 'kick', 'rbr', 'rbryenm', 'лшсл')
tp = ('tp', 'тп', 'телепортировать', 'teleport')
donate = ('выдатьдонат', 'givedonate')

# Почему easywl?
# Потому что тупорылый дефолтный вайтлист плохо работает :angryface:

myvkid = 228
# ваш айди в вкк, без кавычек (цифровой именно, не буквенный)
adminsid = (0, 1)
# айди админов, если нужно чтобы серверные команды использовали несколько человек.
# БЕЗ КАВЫЧЕК, ЧЕРЕЗ ЗАПЯТУЮ, если вы единственный админ то введите сюда свой айди ещё раз
grouptoken = ""
# между кавычек въебите свой токен ГРУППЫ, в токене должно быть
# разрешение на отправку сообщений(а лучше вообще все разрешения)
mytoken = ""
# здесь уже ваш личный токен, владельца группы в которой будет этот бот
serverip = ""
# айпи сервера БЕЗ ПОРТА И ДВОЕТОЧИЯ
serverport = ''
# ПОРТ сервера
rconport = 1337
# ркон порт БЕЗ КАВЫЧЕК
rconPass = ""
# ркон пароль, он обязателен!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
donatelink = ""
# ваша ссылка на донат

# тут можно выбрать через какую систему выдавать пермишны, просто поменяйте на нужное значение
permissions = 0
# 0 - пермишны работают через LuckPerms
# 1 - пермишны работают через PermissionsEx

# техническая хуйня
replace = [('[0m', ''), ('[38;5;246m', ''), ('[36;1m', ''), ('[33;1m', ''),
('[38;5;243m', ''), ('[37;1m', ''), ('[33m', ''), ('[31;1m', ''), ('[32m', ''), ('[9m', '')]



playerDict = {'айди вк игрока': 'его ник',
              'его ник' : 'айди вк игрока'}
# команда на добавление игроков в  этот список есть (добигрок {вкАйди} {ник}), можно не заполнять это руками :)

np.save('playersdict.npy', playerDict) # ЗАПУСТИТЕ ЭТОТ ФАЙЛ И УДАЛИТЕ ЭТУ СТРОКУ И ЕЩЁ САМУЮ ПЕРВУЮ!!!!
