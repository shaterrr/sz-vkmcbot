# sz-vkmcbot
Чо эта за хуйня и с чем её хавают?

Эта кароче бот для вашего, так сказать, сервера майнкрафт. Обьясню на примере

Вот есть у вас сервер, да, и лежите вы такой на кровате бабосики считаете с донатов  
И тут вам говоярт "А вот Vasyan228 читерит!!! Забань его!!!", а тебе так лень с кровати вставать или в консоль сервера заходить ШО ПИЗДЕЦ  
На помощт приходит мой невьебенный охуенный бот который позволяет отправлять РКОН команды (ну типа как обычно ты в майне команды вводишь, тока это удаленно) на сервер  
И ты такой написал в вк "забанить Vasyan228 10y Пидорас с читами!"  
Какой итог? Васян забанен, ты лежишь в кроватке, все счастливы кроме васяна  

я вот эту хуйню щас сижу  пишу на серьезных щах, не дай бог я на собеседование пойду а там вот это увидят =)

# А как эту залупу включить то, ебана рот
Сперва НАПЕРВО тебе надо включить RCON на своём сервере, а также создать токены в вк у своей группы и своего профиля (если ты владелец группы конечно же), обьяснять не буду, сам найди ёпта. Также установить на машину где этот код будет работать питон и библиотеки для него. Для этого в консоли (линукса или cmd просто)  
- pip install mctools
- pip install mcstatus
- pip install vk-api  
И всё

А далее просто: Скачиваешь эти два питон файла, вставляешь их в одну папку, далее заходишь в slovarik.py и вводишь все данные которые я там расписал.  
Думаю поймёшь, там всё закоменчено шо пиздец,только дебил не поймёт. Чтобы бот заработал тебе нада запустить(именно запустить скрипт, не просто открыть его) vkbot.py  
Ну и всё, если не еблан то должно заработать. Подожди после запуска минутку, если бот написал "бот запущен", то значит бот запущен. А если написал **"Ошибка  подключения к серверу по причине блаблабла"** то ты чота налажал, это уже не мои проблемы XDD (ну чиркани там https://vk.com/szarkan, обьясню чо куда)  

## Список команд
Команды доступные всем:
- пинг - выводит пинг сервера и кол-во текущих игркоов
- игроки - выводит команду /list
- пися - попа
- донат - отправится ссылка из **slovarik.py** на покупку доната
~~- ! перед сообщением - перенаправляет сообщение пользователя ВСЕМ админам из списка.~~ Ломает бота, потом пофикшу

командны доступные **только админам**:
- ban {игрок} {время} {причина} - очевидно банит игрока. Бан происходит с помощью essentials, и поэтому {время} принимается только вида 10m, 5m, 6days и т.п. Причина кстати пишется в одно слово, иначе вылезет ошибка :)
- ban {игрок} {причина} - тоже самое, только пермач, если у вас нет никаких essentials и прочего для бана игроков - используйте это  
- unban {игрок} - разбан игрока командой /pardon (принимается как и essentials, так и дефолт майнкрафтом)
- kick {игрок} {причина} - кикает игрока,  причина также пишется в одно слово. Можно не писать причину, кикнет без причины
- tp {игрок} {x} {y} {z} - тпшит игрока по координатам, принимает также тильды типа ~ ~10 ~
- всем: - пишет на сервер сообщение через команду say (дефолт майнкрафт команда, принимает цветовые коды майнкрафтовские)
- если перед сообщением / - отправляет команду которую вы введете, ну типа если просто надо команду ввести которой нет в списке (/execute, /reload и т.п.)
- вл {добавить/удалить} {игрок} - добавить игркоа в вайтлист или удалить  
- выдатьдонат {название привелегии} {игрок} {время} - выдаь донат через Luckperms, время принимается вида 10y, 5days, 1minute и т.п.

![Снимок экрана 2022-04-07 232357](https://user-images.githubusercontent.com/50948836/162289938-675e03bd-c3c5-4f4a-a3e6-6b3ad34f9d58.png)

У всех команд есть свои вариации, они записаны в **slovarik.py**, вы их можете спокойно изменять!!111  

# Контактики
Если вам нужна команда лично для вас, или же там чета не работает ну или вам помощь нужна - https://vk.com/szarkan, чирканите, обкашляем  
Все обновления бота будут выкладываться сюдааа - https://discord.gg/SfuPJkWs  

бота можете спокойно использовать
весь проект защищён лицензией "не воруйте пожалуйста скрипты, моя зарплата - деньги на обед от мамы"
