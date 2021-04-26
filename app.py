# Импортируем библиотеки
from tkinter import *
import pymongo
from pymongo import MongoClient
import dns
from datetime import datetime

# Подключение и настройка MongoDB
client = pymongo.MongoClient("mongodb+srv://Dmitry:PyeWxW4ulFZr7M7M@messages.f8s3p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.Messages
collection = db.Messages
# Настройка окна
win = Tk()
win.title('Мессенджер')
win.geometry('312x348')
win['bg'] = '#E8FFDA'

messages = [] # Массив с уже существующими сообщениями

# Начальный вывод сообщений
for message in collection.find({}):
		messages.append(Label(win, bg  = '#E8FFDA',text = message['time']).pack())
		messages.append(Label(win, bg  = '#E8FFDA',text = message['text']).pack())

# Функция, вставляющая сообщение в базу данных и обратно из базы данных в Label
def send_message():
	time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Время отправки сообщения
	collection.insert_one({
		'time': time,
		'text':e_input.get()
		})
	last_message = collection.find_one({'text':e_input.get()})
	Label(win, bg  = '#E8FFDA',text = last_message['time']).pack()
	Label(win, bg  = '#E8FFDA',text = last_message['text']).pack()

	l_message['text'] = None
# Ввод сообщения
e_input = Entry(win,
				bg = 'white',
				border = 1,
				font = ('Roboto',10))

e_input.place(relx = 0.02,
                             rely = 0.9,
                             relheight = 0.08, 
                             relwidth = 0.7)

# Кнопка
b_send = Button(win,
				text = 'Отправить',
				bg = 'white',
				font = ('Roboto',10),
				border = 1,
				command = send_message)

b_send.place(relx = 0.75,
            rely = 0.9,
            relheight = 0.07, 
            relwidth = 0.22)

# Поле сообщений
l_message = Label(win, bg  = '#E8FFDA')
l_message.place(relx = 0.02, rely = 0.03)

win.mainloop()