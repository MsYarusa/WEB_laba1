import socket
import pygame as pg

PORT_SENDER = 3333
PORT_RECEIVER = 5050
IP = "10.23.30.101"
MSG_SIZE = 1024
WIN_SIZE = (800, 640)
STOP_MSG = 'break'


class Client:
    def __init__(self, ip, port_sender, port_receiver):
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sender.connect((ip, port_receiver))
        self.receiver.connect((ip, port_sender))
        self.number = ""

    def run(self):
        screen = pg.display.set_mode(WIN_SIZE)
        pg.display.set_caption('Клиент')

        running = True
        while running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.sender.send(STOP_MSG.encode())
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    data = (str(event.pos[0]) + ' ' + str(event.pos[1]))
                    data_bytes = data.encode()
                    self.sender.send(data_bytes)

            image_bytes = self.receive()
            image = pg.image.frombuffer(image_bytes, WIN_SIZE, 'RGB')
            screen.blit(image, (0, 0))
            pg.display.flip()

        client.close()

    def get_data(self, bytes_count):

        data = b''
        while len(data) < bytes_count:
            part = self.receiver.recv(bytes_count - len(data))
            data += part
        return data

    def receive(self):

        data = b''
        while True:
            part_len = int.from_bytes(self.get_data(2), "big")
            if part_len == 0:
                return data
            data += self.get_data(part_len)


client = Client(IP, PORT_SENDER, PORT_RECEIVER)
client.run()



