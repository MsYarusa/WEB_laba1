import socket
import pygame as pg
import window
import threading

PORT_SENDER = 3333
PORT_RECEIVER = 5050
IP = "192.168.43.163"
MSG_SIZE = 1024
WIN_SIZE = (520, 520)
STOP_MSG = 'break'


class Client:
    def __init__(self, port_sender, port_receiver):
        self.port_sender = port_sender
        self.port_receiver = port_receiver
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        connection = threading.Thread(target=self.connect)
        connection.start()
        window.root.mainloop()

    def connect(self):
        trying = True
        while trying:
            try:
                self.sender.connect((window.IP, self.port_receiver))
                self.receiver.connect((window.IP, self.port_sender))
                window.send_conf()
                trying = False
            except:
                window.send_error()

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
            if image_bytes != b'':
                image = pg.image.frombuffer(image_bytes, WIN_SIZE, 'RGB')
                screen.blit(image, (0, 0))
            pg.display.flip()

        self.sender.close()
        self.receiver.close()

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


client = Client(PORT_SENDER, PORT_RECEIVER)
client.run()



