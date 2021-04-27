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
win.resizable(width=False, height=False)

messages = [] # Массив с уже существующими сообщениями в мессенджере
length_of_collection = [] # Длина массива с документами, содержащимися в коллекции в БД

# Начальный вывод сообщений
for message in collection.find({}):
		messages.append(Label(win, bg  = '#E8FFDA',text = (message['name'] + ' ' + message['time'])).pack())
		messages.append(Label(win, bg  = '#E8FFDA',text = message['text']).pack())

# Функция, считающая длину массива с документами и её вызов
def count_docs():
	length_of_collection = []
	for doc in collection.find():
		length_of_collection.append(doc)
	return(len(length_of_collection))

# Функция, проверяющая, появилось ли новое сообщение в БД, и добавляющая его в оконо сообщений
def upd_messages():
	message = list(collection.find().sort('time',-1).limit(1))
	if len(messages) < count_docs()*2:
		messages.append(Label(win, bg  = '#E8FFDA',text = (name + ' ' + message[0]['time'])).pack())
		messages.append(Label(win, bg  = '#E8FFDA',text = message[0]['text']).pack())

	win.after(5000, upd_messages)
upd_messages()


# Функция, вставляющая сообщение в базу данных и обратно из базы данных в Label
def send_message():
	time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Время отправки сообщения
	collection.insert_one({
		'name': name,
		'time': time,
		'text':e_input.get()
		})
	last_message = collection.find_one({'text':e_input.get()})
	messages.append(Label(win, bg  = '#E8FFDA',text = (name + ' ' + last_message['time'])).pack())
	messages.append(Label(win, bg  = '#E8FFDA',text = last_message['text']).pack())

# Функция, регистрирующая имя пользователя и закрывающая приветственное окно
def name_reg():
	global name
	if e_enter.get() != '':
		name = e_enter.get()
		start_win.destroy()

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

# Поле ввода имени
start_win = Frame(win) #Фрейм, на котором будет вводиться имя
start_win.place(relheight = 1, 
            relwidth = 1)
l_enter = Label(start_win, text = 'Добро пожаловать\nВведите имя') # Приветственная надпись
l_enter.place(rely = 0.3, relx = 0.3)
e_enter = Entry(start_win) # Ввод
e_enter.place(relx = 0.1,
            rely = 0.5,
			relheight = 0.07, 
            relwidth = 0.5)
b_enter = Button(start_win, text = 'Войти', command = name_reg) # Кнопка входа
b_enter.place(relx = 0.7,
            rely = 0.5,
			relheight = 0.07, 
            relwidth = 0.2)

###############################

win.mainloop()