from app import app, db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(255))
	role = db.Column(db.String(20))