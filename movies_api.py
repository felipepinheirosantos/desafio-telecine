from flask import json
import requests

#Connect to TheMovieDB database to search movies based on name or release year
def getMovies(name):

	url = "https://api.themoviedb.org/3/search/movie?api_key=8f40184a1ca7cdc6e790a73ac62f9677&language=pt-BR"
	
	if(name):
		url += "&query="+ name
		r = requests.get(url)
		data = json.loads(r.text);
		return data['results']