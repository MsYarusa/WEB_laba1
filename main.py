import socket
import threading
import game

PORT = 3333
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


MSG_SIZE = 1024
STOP_MSG = 'break'
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2.bind((SERVER, 5050))


def start():
    server.listen()
    server2.listen()
    win = threading.Thread(target=game.start_game)
    win.start()
    while True:
        client, addr = server.accept()
        client2, addr = server2.accept()
        thread = threading.Thread(target=process_client, args=(client, addr))
        thread.start()
        thread2 = threading.Thread(target=process_client2, args=(client2, addr))
        thread2.start()
        print(f"[АКТИВНЫЕ СОЕДИНЕНИЯ] {threading.active_count() - 2}")


def reliable_send(self, data: bytes) -> None:
    """
    Функция отправки данных в сокет
    Обратите внимание, что данные ожидаются сразу типа bytes
    """
    # Разбиваем передаваемые данные на куски максимальной длины 0xffff (65535)
    for chunk in (data[_:_+0xffff] for _ in range(0, len(data), 0xffff)):
        print('processing...')
        self.send(len(chunk).to_bytes(2, "big")) # Отправляем длину куска (2 байта)
        self.send(chunk) # Отправляем сам кусок
    print('finished')
    self.send(b"\x00\x00") # Обозначаем конец передачи куском нулевой длины


def process_client(client, addr):
    print(f"[НОВОЕ СОЕДИНЕНИЕ] {addr} подключился")

    connected = True
    while connected:

        data_im = game.pg.image.tostring(game.buff_screen, 'RGB')
        reliable_send(client, data_im)

    print("[СОЕДИНЕНИЕ ПРЕРВАНО...]")


def process_client2(client2, addr):
    print(f"[НОВОЕ СОЕДИНЕНИЕ] {addr} подключился")

    # client.send("ПРИВЕТ".encode())
    # print(client.recv(1024).decode())
    # client.send("ПОКА".encode())

    connected = True
    while connected:
        print('waiting for data')
        data = client2.recv(MSG_SIZE).decode()
        print('got_data')
        if data == STOP_MSG:
            connected = False

        game.buffer.append(data.split())

    print("[СОЕДИНЕНИЕ ПРЕРВАНО...]")


print("[СЕРВЕР ЗАПУСКАЕТСЯ...]")
start()




