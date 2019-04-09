from flask import json
import requests

#Connect to TheMovieDB database to search movies based on name or release year
def getMovies(name):
	url = "https://api.themoviedb.org/3/search/movie?api_key=8f40184a1ca7cdc6e790a73ac62f9677&language=pt-BR&query="+ name
	r = requests.get(url)
	data = json.loads(r.text);
	return data['results']


#Connect to TheMovieDB database to get all the cast from a movie
def getCast(id):
	r = requests.get(" https://api.themoviedb.org/3/movie/"+ str(id) +"/credits?api_key=8f40184a1ca7cdc6e790a73ac62f9677")    
	data = json.loads(r.text);
	return data['cast']


#Connect to TheMovieDB database to get the genre name of the movies
def getGenre(genre_id):
	r = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=8f40184a1ca7cdc6e790a73ac62f9677&language=pt-BR")    
	data = json.loads(r.text);

	genres = data['genres']

	for genre in genres:
		if(genre['id'] == genre_id):
			return genre['name']