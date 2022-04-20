from mctools import RCONClient

serverip = "45.93.200.49"
serverport = '25578'
rconport = 17578
rconPass = "S3cTxfvk2A"

rcon = RCONClient(serverip, port=rconport)  # подключаемся к ркону
connect = rcon.login(rconPass)  # вводим пароль ркона

def getIp():
    f = open('players.txt', 'r')
    com = rcon.command("authme getip Szarkan")
    print(com)
    print(f.readlines(116))

getIp()