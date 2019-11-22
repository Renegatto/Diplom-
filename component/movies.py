from bs4 import BeautifulSoup
import requests

def movies_url():
	url = BeautifulSoup(requests.get('https://afisha.tut.by/film/').text, 'lxml')
	return url

def data_movies():
	films = movies_url().find('div', class_='events-block js-cut_wrapper').find_all('li')
	movies = list()

	for data in films:
	    temp = dict()
	    temp['name'] = data.find('img').get('alt')
	    temp['link'] = data.find('a').get('href')
	    temp['image'] = data.find('img').get('src')
	    temp['info'] = data.find('div').find('p').text
	    movies.append(temp)
	return movies

def bot_movies():
	url = movies_url()
	articles = url.find_all('ul', {'class': ['b-lists list_afisha col-5']})
	return [art.find('a', {'class': ['name']}).find('span').get_text() for art in articles]