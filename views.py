from flask import jsonify, request, make_response
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid, jwt, datetime
from models import User
from functools import wraps

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
			data = jwt.decode(token, app.config['SECRET_KEY'])
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
		
		token = jwt.encode({ 'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
		return jsonify({ 'token' : token.decode('UTF-8') })

	return make_response('Could not verify the access data', 401, { 'WWW-Authenticate' : 'Basic realm="Login required!"'})


#create new users
@app.route('/user/create', methods=['POST'])
def createUsers():
	data = request.get_json()
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