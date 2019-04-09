from flask import jsonify, request
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from models import User

@app.route('/')
def home():
    return "Desafio Telecine"


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
def getUsers():

	users_list = User.query.all()

	output = []

	for user in users_list:
		user_data = {}
		user_data['name'] = user.name
		user_data['public_id'] = user.public_id
		user_data['role'] = user.role

		output.append(user_data)

	return jsonify(output), 200