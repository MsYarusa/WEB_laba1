import socket
import pygame as pg


def readexactly(self, bytes_count: int) -> bytes:
    """
    Функция приёма определённого количества байт
    """
    b = b''
    while len(b) < bytes_count: # Пока не получили нужное количество байт
        part = self.recv(bytes_count - len(b)) # Получаем оставшиеся байты
        if not part: # Если из сокета ничего не пришло, значит его закрыли с другой стороны
            raise IOError("Соединение потеряно")
        b += part
    return b


def reliable_receive(self) -> bytes:
    """
    Функция приёма данных
    Обратите внимание, что возвращает тип bytes
    """
    b = b''
    while True:
        part_len = int.from_bytes(readexactly(client, 2), "big") # Определяем длину ожидаемого куска
        if part_len == 0: # Если пришёл кусок нулевой длины, то приём окончен
            return b
        b += readexactly(client, part_len) # Считываем сам кусок


PORT = 3333
SERVER = "10.193.180.134"
ADDR = (SERVER, PORT)
MSG_SIZE = 1024
WIN_SIZE = (800, 640)
FORMAT = 'utf-8'
STOP_MSG = 'break'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect((SERVER, 5050))

# print(client.recv(1024).decode())
# print(client.recv(1024).decode())
# client.send("HI".encode())


screen = pg.display.set_mode(WIN_SIZE)
pg.display.set_caption('Клиент')

running = True
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            data = STOP_MSG.encode()
            client2.send(data)
            running = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            data = (str(event.pos[0]) + ' ' + str(event.pos[1]))
            data_bytes = data.encode()
            client2.send(data_bytes)

    image_code = reliable_receive(client)
    image = pg.image.fromstring(image_code, WIN_SIZE, 'RGB')
    screen.blit(image, (0, 0))
    pg.display.flip()

client.close()



