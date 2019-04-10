from flask import jsonify, request, make_response, Response, json
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid, jwt, datetime, movies_api
from models import User
from functools import wraps
import datetime

@app.route('/')
def home():
    return "Desafio Telecine"

#Receive token in headers an try to load user's public_id
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']

		if not token:
			return jsonify({ 'error' : 'Token is missing' }), 401

		try: 
			data = jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')
			current_user = User.query.filter_by(public_id=data['public_id']).first()
		except:
			return jsonify({ 'error' : 'Token is invalid' }), 401

		return f(current_user, *args, **kwargs)

	return decorated


#Receive user login and pass to generate a token to authorize access
@app.route('/authenticate')
def login():
	auth = request.authorization

	if not auth or not auth.username or not auth.password:
		return make_response('Could not verify the access data ', 401, { 'WWW-Authenticate' : 'Basic realm="Login required!"'})

	user = User.query.filter_by(name=auth.username).first()

	if not user:
		return make_response('Could not verify the access data', 401, { 'WWW-Authenticate' : 'Basic realm="Login required!"'})
	
	if check_password_hash(user.password, auth.password):
		
		token = jwt.encode({ 'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256').decode('UTF-8')
		return jsonify({ 'token' : token })

	return make_response('Could not verify the access data', 401, { 'WWW-Authenticate' : 'Basic realm="Login required!"'})


#create new users
@app.route('/user/create', methods=['POST'])
def createUsers():
	data = request.get_json()

	if(not data['password']):
		return jsonify({ 'message' : 'User created with success' }), 401

	hashed_password = generate_password_hash(data['password'], method='sha256')

	new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, role='user')
	db.session.add(new_user)
	db.session.commit()

	return jsonify({ 'message' : 'User created with success' }), 200


#get users list
@app.route('/users')
@token_required
def getUsers(current_user):

	users_list = User.query.all()

	output = []

	for user in users_list:
		user_data = {}
		user_data['name'] = user.name
		user_data['public_id'] = user.public_id
		user_data['role'] = user.role

		output.append(user_data)

	return jsonify(output), 200

#Route to get and format movies based on search by name
@app.route('/movie/<name>', methods=['GET'])
@token_required
def getMoviesBySearch(current_user, name):

	results = movies_api.getMovies(name)

	if(results):

		output = { 'movies' : [] }

		for movie_data in results:
			data = {}
			item = { 'item' : {} }

			data['title'] = movie_data['original_title']
			data['brazilian_title'] = movie_data['title']
			data['release_date'] = ''
			if(movie_data['release_date']):
				release_date = datetime.datetime.strptime(movie_data['release_date'], '%Y-%m-%d')
				data['release_date'] = release_date.year

			cast = movies_api.getCast(movie_data['id'])
			data['cast'] = []
			
			genres = []
			for genre_id in movie_data['genre_ids']:
				genre_name = movies_api.getGenre(genre_id)
				genres.append(genre_name)

			data['genres'] = ', '.join(genres)

			for person in cast:
				if person['character']:
					person_data = {
						'role' : person['character'],
						'name' : person['name']
					}
					data['cast'].append(person_data)


			item['item'].update(data)
			output['movies'].append(item)

		return Response({ json.dumps(output) }, mimetype='application/json')

	return jsonify({ 'message' : 'Movie not found.' }), 200