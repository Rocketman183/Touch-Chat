# Импортируем библиотеки
from tkinter import *
from tkinter import ttk
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
win.title('Touch chat')
win.geometry('312x348')
win['bg'] = '#E8FFDA'
win.resizable(width=False, height=False)

# Создание скроллбара
main_frame = Frame(win,bg = '#E8FFDA') # Создание мэйнфрейма
main_frame.pack(fill=BOTH, expand=1)

# Создание Canvas
my_canvas = Canvas(main_frame, width = '290', bg = '#E8FFDA')
my_canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

# Добавление скроллбара в Canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

# Конфигурация Canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
def _on_mouse_wheel(event):
    my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
# Создание 2 фрейма
second_frame = Frame(my_canvas, bg = '#E8FFDA')

# Создание окна в Canvas
my_canvas.create_window((0,0), window=second_frame, width = '300', height = '1000')

messages = [] # Массив с уже существующими сообщениями в мессенджере
length_of_collection = [] # Длина массива с документами, содержащимися в коллекции в БД

# Поле сообщений
message_area = Frame(second_frame, bg = '#E8FFDA')
message_area.place(relwidth=1, relheight = 1)

# Начальный вывод сообщений
for message in collection.find({}):
		messages.append(Label(message_area, bg = '#E8FFDA', text = (message['name'] + ' ' + message['time']), font = ('Arial',10, 'bold')).pack())
		messages.append(Label(message_area, bg = '#E8FFDA', text = message['text'], font = ('Arial', 10)).pack())

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
		messages.append(Label(message_area, bg  = '#E8FFDA',text = (name + ' ' + message[0]['time']), font = ('Arial',10, 'bold')).pack())
		messages.append(Label(message_area, bg  = '#E8FFDA',text = message[0]['text'], font = ('Arial',10)).pack())

	win.after(5000, upd_messages)
upd_messages()

# Функция, вставляющая сообщение в базу данных и обратно из базы данных в Label
def send_message():
	if e_input.get() != '':
		time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Время отправки сообщения
		collection.insert_one({ # Отправка в БД
			'name': name,
			'time': time,
			'text':e_input.get()
			})
		last_message = collection.find_one({'text':e_input.get()}) # Вставка из БД в окно сообщений
		messages.append(Label(message_area, bg  = '#E8FFDA',text = (name + ' ' + last_message['time']), font = ('Arial',10, 'bold')).pack())
		messages.append(Label(message_area, bg  = '#E8FFDA',text = last_message['text'], font = ('Arial',10)).pack())
		e_input.delete(0, END) # Очистка поля ввода после отправки
		e_input.insert(0, "")

def send_message_enter(self):
	if e_input.get() != '':
		time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Время отправки сообщения
		collection.insert_one({ # Отправка в БД
			'name': name,
			'time': time,
			'text':e_input.get()
			})
		last_message = collection.find_one({'text':e_input.get()}) # Вставка из БД в окно сообщений
		messages.append(Label(message_area, bg  = '#E8FFDA',text = (name + ' ' + last_message['time'])).pack())
		messages.append(Label(message_area, bg  = '#E8FFDA',text = last_message['text']).pack())
		e_input.delete(0, END) # Очистка поля ввода после отправки
		e_input.insert(0, "")

# Функция, регистрирующая имя пользователя и закрывающая приветственное окно
def name_reg():
	global name
	if e_enter.get() != '':
		name = e_enter.get()
		start_win.destroy()

# Поле ввода и отправки
input_send = Frame(win, bg = 'green')
input_send.place(relwidth=1, relheight = 0.1, relx = 0, rely = 0.9)
# Ввод сообщения
e_input = Entry(input_send,
				bg = 'white',
				border = 1,
				font = ('Roboto',10))

e_input.place(relx = 0.02,
                             rely = 0.1,
                             relheight = 0.8, 
                             relwidth = 0.7)

# Кнопка
b_send = Button(input_send,
				text = 'Отправить',
				bg = 'green',
				font = ('Roboto',10),
				border = 1,
				command = send_message)

b_send.place(relx = 0.75,
            rely = 0.1,
            relheight = 0.8, 
            relwidth = 0.22)

win.bind('<Return>', send_message_enter)

# Поле ввода имени
start_win = Frame(win, bg = '#292825') #Фрейм, на котором будет вводиться имя
start_win.place(relheight = 1, 
            relwidth = 1)
l_enter = Label(start_win, text = 'Добро пожаловать!\nВведите имя:', font = ('Arial',15,'bold'), bg = '#292825', fg = '#FFA300') # Приветственная надпись
l_enter.place(rely = 0.3, relx = 0.17)
e_enter = Entry(start_win) # Ввод
e_enter.place(relx = 0.1,
            rely = 0.5,
			relheight = 0.07, 
            relwidth = 0.5)
b_enter = Button(start_win, text = 'Войти', command = name_reg, bg = '#292825', fg = '#FFA300', activebackground = '#292825', activeforeground = '#FFA300') # Кнопка входа
b_enter.place(relx = 0.7,
            rely = 0.5,
			relheight = 0.07, 
            relwidth = 0.2)

win.mainloop()