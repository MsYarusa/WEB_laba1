from tkinter import *
import time


def get_ip():
    global IP
    global button_clicked
    IP = entry.get()
    button_clicked = True
    time.sleep(0.01)


def send_error():
    if button_clicked:
        error_label["text"] = "Ошибка"


def send_conf():
    error_label["text"] = "Подключено"
    error_label["foreground"] = "green"
    time.sleep(0.5)
    root.destroy()


IP = ""
root = Tk()
root.title('Подключение...')
root.geometry('300x120+660+400')
root.resizable(width=False, height=False)

label = Label(root, font="Calibri 13", text="Введите IP хоста чтобы подключиться")
label.pack(padx=5, pady=5, anchor=NW)

f_bot = Frame(root)
f_bot.pack()
entry = Entry(f_bot, font="Calibri 20", width=15)
entry.pack(side=LEFT, ipadx=5)

button = Button(f_bot, text="Ввести", height=1, font="Calibri 13")
button_clicked = False
button["command"] = get_ip
button.pack(side=LEFT)

error_label = Label(foreground="red", text="", wraplength=250, font="Calibri 13")
error_label.pack(padx=5, pady=10, anchor=NW)