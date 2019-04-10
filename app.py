from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/desafio-telecine.db'
app.config['SECRET_KEY'] = 'pynheiro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

import views
from models import User

admin = User.query.filter_by(name='admin_test').first()

if not admin:
	hashed_password = generate_password_hash('123456', method='sha256')

	admin = User(name='admin_test', password=hashed_password, public_id=str(uuid.uuid4()), role='admin')
	db.session.add(admin)
	db.session.commit()