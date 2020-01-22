#!/usr/bin/python3

'''
KORPUS
Вступительное задание 


1.Описание ситуации
 
Вы помогаете организаторам школьных соревнований по лыжной гонке. Одна 
из задач организаторов - обеспечить всех одинаковой смазкой для лыж. 
Участников очень много, надо купить один вид на всех. Соревнования 
проходят в воскресенье, поставщик смазки может продать не позднее 
пятницы. Соревнования проходят в Челябинске в парке Гагарина.
 
2.Задание
 
Надо написать программу, которая получит прогноз погоды на ближайшее 
воскресение и подскажет нужный вид смазки.
 
3. Подсказка
 
Смазка выбирается следующим образом:
a) если температура воздуха -13 градусов Цельсия и холоднее рекомендуйте
покупать смазку “Type C”.
b) Если от -13 до -5, то подойдет “Type B”.
c) Если теплее -5, то только “Type A”.
 
4. Требования
 
1)    Программа должна быть реализована на Python любой версии.
2) Код решения опубликуйте на https://repl.it, нам пришлите только 
ссылку на ваш проект. 
3) Чтобы мы могли проверить работу программы - напишите инструкцию как с
ней работать. А еще лучше выведите все в консоль, а код документируйте.
 
5. Рекомендации
 
Желательно, но не обязательно, прогноз погоды получать через API. 
Сервисов поставщиков масса, берите любой. Если он отдает данные в json, 
то рекомендуем использовать модуль requests. В нем есть удобный метод 
json(), преобразующий json-ответ в словарь.

6. Только развитие! Только хардкор!
 
Все остальные детали  - на ваше усмотрение. Если что-то на ваш взгляд мы
упустили, делайте так, как считаете правильным. Будут вопросы по заданию
- пишете.
 
 
Бонусы
Программировать – это легко и интересно! Мы верим, что вы можете освоить
этот навык самостоятельно. Надо только найти правильный подход. Поэтому 
вот несколько разных курсов, выберите тот, что вам больше понравится:

Простой интерактивый курс на https://www.codecademy.com/learn/learn-pyth
on. На английском. Вполне достаточно бесплатной версии.
Курс от Института биоинформатики https://stepik.org/course/67. На 
русском.
Еще один курс на английском, подробный  - https://www.sololearn.com/Cour
se/Python/.

Дерзайте!
Все курсы доступны бесплатно. Просто выберите тот, что вам больше 
понравится с первых уроков. Если этих курсов мало, посмотрите вот такую 
подбборку - https://tproger.ru/digest/data-science-python/ 
'''

import requests
import datetime
 
# получить appid на openweathermap.org
appid = 'none'

class openweathermap(object):
	url = 'http://api.openweathermap.org/data/2.5/forecast?q={city}\
&units=metric&cnt={cnt}&appid={appid}'
	appid = ''
	city = ''
	cnt = 7*8 # колличество загружаемых записей, на каждый день по 8 
		      # записей, всего 7 дней
	
	def __init__(self, appid, city='Chelyabinsk,RU'):
		self.city = city
		self.appid = appid
	
	def get_weather(self):
		session = requests.Session()
		headers={
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:\
72.0) Gecko/20100101 Firefox/72.0',
			'Accept': '*/*',
			'Accept-Language': 'en-US,en;q=0.5',
		} # На всякий случай прикидываемся браузером
		response = session.get(self.url.format(city=self.city, \
			cnt=self.cnt, appid=self.appid), headers=headers)
		return response.json()
	
	def get_sunday(self):
		out = []
		i = 0
		now = datetime.datetime.now() # получаем текущее время
		c_week = now.isoweekday() # получаем день недели
		timestamp = now.timestamp()
		day_start = datetime.datetime(now.year, now.month, now.day, 0,\
		  0).timestamp() # время в unixtime начало дня
		day_end = datetime.datetime(now.year, now.month, now.day, 23,\
		  59).timestamp() # время в unixtime конца дня
		s = (7 - c_week)*60*60*24 # получаем смещение на воскресенье
		
		weather = self.get_weather()
		timezone = weather['city']['timezone']
		for line in weather['list']:
			if (line['dt'] - timezone >= day_start + s) and \
			  (line['dt']- timezone <= day_end + s):
				# полечаем температуру на воскресенье на каждые 3 часа
				out.insert(i, line)
				i += 1
		return out

if __name__ == '__main__':
	weather = openweathermap(appid)
	average = 0
	j = 0
	i = 0
	for line in weather.get_sunday():
		if i >= 3 and i <= 5: # берем температуру с 9:00 до 15:00
			average += line['main']['temp']
			j += 1
		i += 1
	average /= j # округляем

	print('Средняя температура днем в воскресенье {average} градусов.'.\
	  format(average=round(average,1)))
	if average <= -13:
		print('Следует выбрать смазку “Type C”')
	if average > -13 or average <= -5:
		print('Следует выбрать смазку “Type B”')
	if average > -5:
		print('Следует выбрать смазку “Type A”')
