# sz-vkmcbot
## Чо эта за хуйня и с чем её хавают?  

Эта кароче бот для вашего, так сказать, сервера майнкрафт. Обьясню на примере

Вот есть у вас сервер и лежите вы такой на кровате, бабосики считаете с донатов  
И тут вам пишут "А вот Vasyan228 читерит!!! Забань его!!!", а тебе так лень с кровати вставать или в консоль сервера заходить ШО ПИЗДЕЦ  
На помощт приходит мой невьебенный охуенный бот который позволяет отправлять РКОН команды (ну типа как обычно ты в майне команды вводишь, тока это удаленно) на сервер  
И ты такой написал в ВК боту ```забанить Vasyan228 10лет Пидорас с читами!```  
Какой итог? Васян забанен, ты лежишь в кроватке, все счастливы кроме васяна  

# А как эту залупу включить то, ебана рот
Сперва НАПЕРВО тебе надо включить RCON на своём сервере, это делается в **server.properties**, задать ему пароль!!!!, а также создать токены в вк у своей группы и своего профиля (если ты владелец группы конечно же), обьяснять не буду, сам погугли, это легко. Также установить на машину где этот код будет работать питон и библиотеки для него. Для скачивания библиотек просто введи в консоль эти команды  
```
pip install mctools
pip install mcstatus
pip install vk-api
```
А с питоном сам пожлст разберись  
И всё

А далее просто: Скачиваешь эти два питон файла в **одну папку**, далее заходишь в slovarik.py и вводишь все данные которые я там расписал.  
Думаю поймёшь, там всё закоменчено шо пиздец, только дебил не поймёт. Чтобы бот заработал тебе нада запустить vkbot.py, это делается коммандой ```python vkbot.py```   
Ну и всё, если не еблан то должно заработать. Если бот написал "Бот успешно запущен", то значит бот запущен. А если написал **"Ошибка  подключения к серверу по причине блаблабла"** то он попытается ещё три раза подключиться, но если не получится то значит ты чота налажал, это уже не мои проблемы XDD (ну чиркани там https://vk.com/szarkan, обьясню чо куда)  
Ну и если вк апи упадёт, или ещё какая ошибка, то бот об этом скажет. По крайне й мере должен :-)) xD 🦖

# Список команд
## Команды доступные всем:
- пинг - выводит пинг сервера и кол-во текущих игркоов  
![image](https://user-images.githubusercontent.com/50948836/163648797-514e2c22-489d-46dd-9ce1-823ea9b9d007.png)

- игроки - выводит команду /list  
![image](https://user-images.githubusercontent.com/50948836/163648805-4c4e63f3-3731-471d-aea4-62a9d88cb4bc.png)

- пися - попа  
![image](https://user-images.githubusercontent.com/50948836/163648822-f8e7ce17-07c9-4f53-bc38-2d56d99ee871.png)

- донат - отправится ссылка из **slovarik.py** на покупку доната  
![image](https://user-images.githubusercontent.com/50948836/163648830-b2a3b407-9ed1-4674-9629-ad127933520f.png)

- юмореска - рандомная юмореска из паблика юморески на каждый день  
![image](https://user-images.githubusercontent.com/50948836/163648838-720c116b-f15c-4e1f-ad81-9a91044d24d6.png)

- Если же челикс введет какую-то неизвестную команду, то ему напишет чтобы он написал админу, который записан в переменной **myvkid** в **slovarik.py**  
![image](https://user-images.githubusercontent.com/50948836/163648846-8ab9750b-dcf7-4b19-ae58-25661bf5da32.png)


## командны доступные **только админам**:

- бан {игрок} {время} {причина} - очевидно банит игрока. Бан происходит с помощью essentials, и поэтому {время} принимается только вида 10m, 5m, 6days и т.п.  
![image](https://user-images.githubusercontent.com/50948836/163648929-f5ee2b3a-147e-4790-a916-29d4d0998741.png)

- пермач {игрок} {причина} - тоже самое, только пермач, если у вас нет никаких essentials и прочего для бана игроков - используйте это  
Фотки пока нет! хыхых  
- разбан {игрок} - разбан игрока командой /pardon (принимается как и essentials, так и дефолт майнкрафтом)  
![image](https://user-images.githubusercontent.com/50948836/163648953-31019444-0566-4e52-8d68-e28339549787.png)

- kick {игрок} {причина} - кикает игрока. Можно не писать причину, кикнет без причины  
![image](https://user-images.githubusercontent.com/50948836/163649031-77f58e50-55c1-4497-836c-28937709f1d7.png)

- tp {игрок} {x} {y} {z} - тпшит игрока по координатам, принимает также тильды типа ~ ~10 ~, но тильды телепортируют относительно мирового спавна!  
![image](https://user-images.githubusercontent.com/50948836/163649075-176a2694-ea0c-4a1f-919a-41ff457795ea.png)

- всем: {сообщение} - пишет на сервер сообщение через команду say (дефолт майнкрафт команда, принимает цветовые коды майнкрафтовские)  
![image](https://user-images.githubusercontent.com/50948836/163649086-ce6b333b-9642-4bcb-8203-205803413e7c.png)

- ком {команда без слеша} - отправляет команду которую вы введете, ну типа если просто надо команду ввести которой нет в списке (/execute, /reload и т.п.)  
![image](https://user-images.githubusercontent.com/50948836/163649121-903b5703-8108-4b10-a44e-fd61c63ad605.png)

- вл {добавить/удалить} {игрок} - добавить игркоа в вайтлист или удалить  
![image](https://user-images.githubusercontent.com/50948836/163649151-198a2506-d593-4eae-bb61-ffbe2f678ca3.png)

- выдатьдонат {игрок} {название привелегии} {время} - выдать донат через Luckperms или PermissionsEX(настраивается в **slovarik.py**).  
![image](https://user-images.githubusercontent.com/50948836/163649170-3d5fe665-da23-4c19-b756-0458ca663e57.png)  

- перезагрузись - перезагружает бота  
![image](https://user-images.githubusercontent.com/50948836/164236106-e31ff831-a484-485a-8164-0f73fe78d6b5.png)  

- выключись - выключает бота  
![image](https://user-images.githubusercontent.com/50948836/164236159-0ed30b64-5200-483c-89e6-31cfd2d4a4a8.png)

В LuckPerms время принимается вида 10y, 5days, 1minute и т.п, в PEX привелегия даётся перманентно.  


У всех команд есть свои вариации, они записаны в **slovarik.py**, вы их можете спокойно изменять!!111  
Выбрать между LuckPerms и PEX можно там же, там всё написано как это делаетца
Также почти в каждой команде есть обработка ошибок, тоесть если вы захотите телепортировать игрока которого нет на сервере, то вам скажут об этам!!!

# Контактики
Если вам нужна команда лично для вас, или же там чета не работает ну или вам помощь нужна - https://vk.com/szarkan, чирканите, обкашляем  

бота можете спокойно использовать, главное напишите что вы его используете чтобы я понял какой я крутой погромист  

Код защищён лицензией MIT (делайте чо хотите, только мне об этом напишите в вк)
