# sz-vkmcbot
## Что это за хуетень?  

Эта кароче бот для вашего, так сказать, сервера майнкрафт. Посылать всякие очень полезные команды на ваш сервер.      
Но это нетолько! Этот бот обрабатывает заявки игроков в вайтлист, делает список игроков, с помощью которого вы можете быстро узнать ВК игрока, имеет слабенький но всё же интеллект, имеет просто прикольные команды, да и будет полезным каждому админиксу

# А как эту залупу включить то, ебана рот   
1. Включаеш РКОН на сервере своем залупском, добавляешь ему пароль   
2. В своей группе ВК берешь токен со всеми разрешениями, не знаешь как - погугли. То же самое сделай с токеном от своего профиля   
2. В файл ```slovarik.py``` добавляешь все значения которые там указаны, ВСЕ БЛЯТЬ!   
(сичас я буду объяснять для серверов на линуксе)   
3. Пишешь в консоль своего хоста ```sudo apt-get update```   
4. Потом ```sudo apt-get install python3``` - это шобы питон скачять   
5. ```sudo apt install python3-pip``` - это хуйня  для питона шобы качать библиотеки   
7. Вот эти команды прописываешь по очереди в консоль:   
```
pip install mctools
pip install mcstatus
pip install vk-api
pip install numpy
```
8. Проверяешь что 6 пункта нет   
9. ???   
10. ПРОФИТ!   

А далее просто: закидываешь все файлики в ***одну папку*** на своём хосте, в консоли прописываешь ```python3 slovarik.py```, и закрываешь. Всё, настройка готова. Теперь надо тебе запустить самого бота, ёбана рот! ```python3 vkbot.py``` пишешь, и ждёшь сообщения себе в ЛС от группы. Должно быть ввида "подключение к РКОН, пингуем сервер, бот успешно запущен". Это значит он запусился, представляеьш?   
Если бот пишет что ошибка подключения какая-то, то фикси, это уже ты налажал, мб ркон не врубил или пароль не ввёл.   
Если бот не пишет ничего впринципе, то ахахаххаах)) (пиши vk.com/szarkan)   
ВКАпи будет падать каждую ночь в 3-5:00 по МСК, этого неизбежать никак, но бот умный, и сам перезапуститься в случае такого падения   
![image](https://user-images.githubusercontent.com/50948836/164236839-b40f4c10-210e-4d2b-a16d-42d71b1dc88d.png)


# Список команд
## Команды доступные всем:   
- команды - выводит список команд, сообщение настраивается в slovarik.py   
![image](https://user-images.githubusercontent.com/50948836/178645798-a17e8024-c33a-4648-a546-fa888282aa99.png)
- заявка - если челикс написал просто слово заявка - то бот отправит гайд по заявке, если не одно слово - то бот перешлёт заявку вам   
![image](https://user-images.githubusercontent.com/50948836/178645939-abebba2c-71d4-4301-87e5-d2a2affeaf7b.png)

- кто {ник игрока или его айди ВК} - на картинке всё понятно. Берёт игроков из списка игроков   
![image](https://user-images.githubusercontent.com/50948836/178646262-775ca818-bbb9-47b8-92f8-22f16c46c99e.png)


- пинг/игроки - выводит пинг сервера и список игроков (тпс всегда будет 20 гигигага)   
![image](https://user-images.githubusercontent.com/50948836/178647294-8d9f55e4-3482-48a1-b648-5c3b6289f0d3.png)


- пися - попа(работает и наоборот)  
![image](https://user-images.githubusercontent.com/50948836/163648822-f8e7ce17-07c9-4f53-bc38-2d56d99ee871.png)

- донат - отправится ссылка из **slovarik.py** на покупку доната  
![image](https://user-images.githubusercontent.com/50948836/163648830-b2a3b407-9ed1-4674-9629-ad127933520f.png)

- юмореска - НЕ РАБОТАЕТ ПОКА ЧТО   
![image](https://user-images.githubusercontent.com/50948836/163648838-720c116b-f15c-4e1f-ad81-9a91044d24d6.png)

- рр - русская рулетка, при проигрыше банит человека на час. Работает только если игрок записан в словарик!!!!!! (команда для добавления ниже в списке)
При смерти игрока, всем админам (или только вам, я не помню) отправится сообщение чтобы проверить  
![image](https://user-images.githubusercontent.com/50948836/173969292-dd6438ae-f04c-47d6-9e24-9812feff64d2.png)

- имитация жизни бота - на некоторые сообщения он может отреагировать по своему. Всё что я смог придумать находиться в конце файла ```vkbot.py```   
![image](https://user-images.githubusercontent.com/50948836/178646586-eccad36c-cac8-4121-b06e-751bf7c5dc52.png)

- Если же челикс введет какую-то неизвестную команду, то ему напишет чтобы он написал админу, который записан в переменной **myvkid** в **slovarik.py**  
![image](https://user-images.githubusercontent.com/50948836/178646613-aaab302c-547f-4b70-9dae-e73abb87dcb2.png)

## команды доступные **стримерам**:   
т.е. тем, кто добавлен в список стримеров

- яснимаю - пишет на сервер предупреждение типа "{ник} начал запись! использование банвордов грозит недельным мутом", а самому стримеру выдаётся прикольный префикс на время   
нет картинки, мне лень   

- янеснимаю - пишет на сервер о том, что игрок перестал снимать, снимает префикс с стримера


## командны доступные **только админам**:
- принять {айди ВК} {ник игрока} - добавить игрока в вайтлист и в список игроков, при этом ему отправится сообщение   
![image](https://user-images.githubusercontent.com/50948836/178646056-53766f59-dc13-41ba-ba0c-3667c9bb3de5.png)

- отклонить {айди ВК} {причина отклонения(необязательно} - отправит сообщение о непринятии заявки, причина необязательна, блять кароч на скрине всё показано   
![image](https://user-images.githubusercontent.com/50948836/178646187-87aa6579-ce15-4375-9aa7-15b68ed815d2.png)

- напиши {айди вк} - если лень заходить в чаты группы, то бот напишет сообщение чуваку   
![image](https://user-images.githubusercontent.com/50948836/178646913-a1abbbde-5524-401e-8892-5471494e6fb3.png)

- айди {ссылка вк} - выдаст айди челвоека по ссылке   
![image](https://user-images.githubusercontent.com/50948836/178646984-df3f9bf9-b70e-4873-9c21-5a6deb8a49f5.png)

- словарь/словарь2 - выводит список игроков(первая команда) и их вк(вторая команда)   
там у меня много игроков, в скрин не влезут, но команда работает


- добигрока {айди ВК} {ник игрока} - Добавить игрока и его вк айди в список   
![image](https://user-images.githubusercontent.com/50948836/178646346-2873f720-68d7-44da-9200-d4a1f0e01583.png)

- удалить {айди ВК или ник} - удалить игрока из списка игроков (лучше не делайте, ники старых игроков всегда понадобятся)   
![image](https://user-images.githubusercontent.com/50948836/178646400-e640c17c-6b4c-463c-88e1-5cab47d9cb0a.png)

- добигрокас {айди ВК} {ник игрока} - Добавить игрока и его вк айди в список стримеров   
нет картинки ббля

- удалитьс {айди ВК или ник} - удалить игрока из списка стримеров   
нет картинки ббля

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

- выключись - выключает бота, при этом включается аварийная версия бота  
![image](https://user-images.githubusercontent.com/50948836/164236159-0ed30b64-5200-483c-89e6-31cfd2d4a4a8.png)

- включи - РАБОТАЕТ ТОЛЬКО НА АВАРИЙНОМ БОТЕ - включает основного бота   
![image](https://user-images.githubusercontent.com/50948836/178648079-2c5aca54-cd6e-45d2-89de-249c77e83247.png)


- кто {ник} - показывает вам ВК игрока, если вы его добавили в словарь конечно  
![image](https://user-images.githubusercontent.com/50948836/173968559-127c88a5-1eda-41fb-a255-ce02a5bc9f19.png)


В LuckPerms время принимается вида 10y, 5days, 1minute и т.п, в PEX привелегия даётся перманентно.  

- Также присутствует логирование всех команд:  
![image](https://user-images.githubusercontent.com/50948836/173970645-84863a24-3ca6-4df7-a2a3-613d25579a20.png)   
Все логи будут в папке с самим кодом под названием ```log.txt```, 20 знаков равно обозначают запуск бота, там кароче он всё логирирует, даже если игрок попытался ввести админскую команду   
Я не знаю нахуя  я это добавил, просто подумал что это крутая идея, че доебался то блять

Если бот выключиться, то запуститься аварийная система, которая будет временно отвечать всем вот такое:   
![image](https://user-images.githubusercontent.com/50948836/178647942-0db6578d-9be2-44d6-81ab-b4716f3cda5e.png)

Это очень помогает, когда хочешь обновление на бота засунуть, но не хочешь подключаться к удалённой машине шобы заново запустить бота


У всех команд есть свои вариации, они записаны в **slovarik.py**, вы их можете спокойно изменять!!111  
Выбрать между LuckPerms и PEX можно там же, там всё написано как это делаетца  
Также почти в каждой команде есть обработка ошибок, тоесть если вы захотите телепортировать игрока которого нет на сервере, то вам скажут об этам!!!

# Контактики
Если вам нужна команда лично для вас, или же там чета не работает ну или вам помощь нужна - https://vk.com/szarkan, чирканите, обкашляем  

бота можете спокойно использовать, главное напишите что вы его используете чтобы я понял какой я крутой погромист  

Код защищён лицензией MIT (делайте чо хотите, только мне об этом напишите в вк)   
Не ручаюсь за правильную работу бота, я как бы ну это самое короче понял да?   
