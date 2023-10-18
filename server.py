import socket
import threading
import game

PORT_SENDER = 3333
PORT_RECEIVER = 5050
IP = socket.gethostbyname(socket.gethostname())

MSG_SIZE = 1024
STOP_MSG = 'break'
FORMAT = 'utf-8'


class Server:
    def __init__(self, ip, port_sender, port_receiver):
        self.ser_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser_receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser_sender.bind((ip, port_sender))
        self.ser_receiver.bind((ip, port_receiver))
        self.window = threading.Thread(target=game.semisapper, args=(ip,))

    def run(self):
        print("[СЕРВЕР ЗАПУСКАЕТСЯ...]")
        self.ser_sender.listen(2)
        self.ser_receiver.listen(2)

        self.window.start()

        while True:
            conn_recv, addr = self.ser_sender.accept()
            conn_send, addr = self.ser_receiver.accept()
            sending = threading.Thread(target=self.send_screen, args=(conn_recv, addr))
            receiving = threading.Thread(target=self.process_conn, args=(conn_send, addr))
            sending.start()
            receiving.start()

    def send_screen(self, conn, addr):

        while True:
            if game.flag:
                data = game.pg.image.tostring(game.buff_screen, 'RGB')

                for chunk in (data[_:_ + 65535] for _ in range(0, len(data), 65535)):
                    conn.send(len(chunk).to_bytes(2, "big"))
                    conn.send(chunk)

                conn.send(b"\x00\x00")
            else:
                conn.send(b"\x00\x00")

    def process_conn(self, conn, addr):
        print(f"[НОВОЕ СОЕДИНЕНИЕ] {addr} подключился")

        connected = True
        while connected:
            data = conn.recv(MSG_SIZE).decode()
            if data == STOP_MSG:
                connected = False

            game.buffer.append(data.split())

        print("[СОЕДИНЕНИЕ ПРЕРВАНО...]")


server = Server(IP, PORT_SENDER, PORT_RECEIVER)
server.run()