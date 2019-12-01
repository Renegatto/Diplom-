import telebot
import pyowm
from component import bot_api, weather_api
from component import data_money, money_list
from component import bot_movies


bot = telebot.TeleBot(bot_api)
owm = pyowm.OWM(weather_api, language = 'ru')

@bot.message_handler(commands=['start'])
def bot_hello(message):
	keyboard = telebot.types.InlineKeyboardMarkup()
	bot_help = telebot.types.InlineKeyboardButton('Помощь',callback_data='/help')
	keyboard.add(bot_help)
	bot.send_message(message.chat.id, 'Здравствуй пользователь, \
для получения команд напишите /help', reply_markup=keyboard)


@bot.callback_query_handler(lambda h: h.data == '/help')
def bot_help(callback_query: telebot.types.CallbackQuery):
	keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
	bot_weather = telebot.types.InlineKeyboardButton('Погода',callback_data='/weather')
	bot_courses_all = telebot.types.InlineKeyboardButton('Курс валют',callback_data='/courses_all')
	bot_movies = telebot.types.InlineKeyboardButton('Фильмы',callback_data='/movies')
	bot_location = telebot.types.InlineKeyboardButton("Геолокация", callback_data='/location')
	keyboard.add(bot_weather, bot_courses_all, bot_movies, bot_location)
	bot.send_message(callback_query.from_user.id, 'Команды на которые я смогу дать ответ: \n\
/weather - Узнать погоду \n/courses - Узнать курс валют на сегодня \n/course_usd - \
Узнать курс Доллара на сегодня \n/course_eur - Узнать курс Евро на сегодня \n\
/course_rub - Узнать курс Российского рубля на сегодня \n/course_uah - Узнать \
курс Гривен на сегодня \n/movies - Узнать какие фильмы сейчас идут \n/location - \
Узнать своё текущее местоположение', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def send_help(message):
	keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
	bot_weather = telebot.types.InlineKeyboardButton('Погода',callback_data='/weather')
	bot_courses_all = telebot.types.InlineKeyboardButton('Курс валют',callback_data='/courses_all')
	bot_movies = telebot.types.InlineKeyboardButton('Фильмы',callback_data='/movies')
	bot_location = telebot.types.InlineKeyboardButton("Геолокация", callback_data='/location')
	keyboard.add(bot_weather, bot_courses_all, bot_movies, bot_location)
	bot.send_message(message.chat.id, 'Команды на которые я смогу дать ответ: \n\
/weather - Узнать погоду \n/courses - Узнать курс валют на сегодня \n/course_usd - \
Узнать курс Доллара на сегодня \n/course_eur - Узнать курс Евро на сегодня \n\
/course_rub - Узнать курс Российского рубля на сегодня \n/course_uah - Узнать \
курс Гривен на сегодня \n/movies - Узнать какие фильмы сейчас идут \n/location - \
Узнать своё текущее местоположение', reply_markup=keyboard)


@bot.callback_query_handler(lambda w: w.data == '/weather')
def bot_weather(callback_query: telebot.types.CallbackQuery):
	weathers = bot.send_message(callback_query.from_user.id, 'В каком районе вас интересует погода?')

	bot.register_next_step_handler(weathers, weather)

@bot.message_handler(commands=['weather'])
def send_weather(message):
	weathers = bot.send_message(message.chat.id, 'В каком районе вас интересует погода?')

	bot.register_next_step_handler(weathers, weather)
def weather(message):
	observation = owm.weather_at_place(message.text)
	w = observation.get_weather()
	temp = w.get_temperature('celsius')['temp']
	bot.send_message(message.chat.id, 'В районе ' + message.text + ' сейчас \
' + w.get_detailed_status()  + ', температура в среднем ' + str(temp) + ' градусов по Цельсию')


@bot.callback_query_handler(lambda c: c.data == '/courses_all')
def bot_course_all(callback_query: telebot.types.CallbackQuery):
	keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
	bot_courses = telebot.types.InlineKeyboardButton('Курc иностранной валюты',callback_data='/courses')
	course_usd = telebot.types.InlineKeyboardButton('Курc Доллара',callback_data='/course_usd')
	course_eur = telebot.types.InlineKeyboardButton('Курс Евро',callback_data='/course_eur')
	course_rub = telebot.types.InlineKeyboardButton('Курс Российского рубля',callback_data='/course_rub')
	course_uah = telebot.types.InlineKeyboardButton('Курс Гривен',callback_data='/course_uah')
	keyboard.add(bot_courses, course_usd, course_eur, course_rub, course_uah)
	bot.send_message(callback_query.from_user.id, 'Какой курс валют вас интересует?', reply_markup=keyboard)

@bot.callback_query_handler(lambda c: c.data == '/courses')
def bot_courses(callback_query: telebot.types.CallbackQuery):
	try:
		money = data_money()
		bot.send_message(callback_query.from_user.id, money)
	except ConnectionError:
		return 404
@bot.message_handler(commands=['courses'])
def send_money(message):
	money = data_money()
	bot.send_message(message.chat.id, money)


@bot.callback_query_handler(lambda c: c.data == '/course_usd')
def course_usd(callback_query: telebot.types.CallbackQuery):
	money = data_money()
	usd = money_list[4]		
	bot.send_message(callback_query.from_user.id, usd +' BYN')

@bot.message_handler(commands=['course_usd'])
def usd(message):
	money = data_money()
	usd = money_list[4]
	bot.send_message(message.chat.id,usd +' BYN')


@bot.callback_query_handler(lambda c: c.data == '/course_eur')
def course_usd(callback_query: telebot.types.CallbackQuery):
	money = data_money()
	eur = money_list[5]
	bot.send_message(callback_query.from_user.id, eur +' BYN')

@bot.message_handler(commands=['course_eur'])
def eur(message):
	money = data_money()
	eur = money_list[5]
	bot.send_message(message.chat.id,eur +' BYN')


@bot.callback_query_handler(lambda c: c.data == '/course_rub')
def course_usd(callback_query: telebot.types.CallbackQuery):
	money = data_money()
	rub = money_list[16]
	bot.send_message(callback_query.from_user.id, rub +' BYN')

@bot.message_handler(commands=['course_rub'])
def rub(message):
	money = data_money()
	rub = money_list[16]
	bot.send_message(message.chat.id, rub +' BYN')


@bot.callback_query_handler(lambda c: c.data == '/course_uah')
def course_usd(callback_query: telebot.types.CallbackQuery):
	money = data_money()
	uah = money_list[2]
	bot.send_message(callback_query.from_user.id, uah +' BYN')

@bot.message_handler(commands=['course_uah'])
def uah(message):
	money = data_money()
	uah = money_list[2]
	bot.send_message(message.chat.id, uah +' BYN')


@bot.callback_query_handler(lambda m: m.data == '/movies')
def course_usd(callback_query: telebot.types.CallbackQuery):
	movies = bot_movies()
	answer = 'Фильмы, которые показывают в кино:\n'
	for m in range(len(movies)):
		answer += f'{movies[m]}\n'
	bot.send_message(callback_query.from_user.id, movies)

@bot.message_handler(commands=['movies'])
def send_movies(message):
	movies = bot_movies()
	answer = 'Фильмы, которые показывают в кино:\n'
	for m in range(len(movies)):
		answer += f'{movies[m]}\n'
	bot.send_message(message.chat.id, movies)


@bot.callback_query_handler(lambda l: l.data == '/location')
def bot_location(callback_query: telebot.types.CallbackQuery):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    location = telebot.types.KeyboardButton('Отправить местоположение', request_location=True)
    keyboard.add(location)
    bot.send_message(callback_query.from_user.id, 'Нажмите пожалуйста на кнопку для передачи своей геолокации', reply_markup=keyboard)

@bot.message_handler(commands=["location"])
def location(message):
	keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
	location = telebot.types.KeyboardButton('Отправить местоположение', request_location=True)
	keyboard.add(location)
	bot.send_message(message.chat.id, 'Нажмите пожалуйста на кнопку для передачи своей геолокации', reply_markup=keyboard)


bot.polling(none_stop = True, interval=2)
