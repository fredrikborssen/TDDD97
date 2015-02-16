import sqlite3
from flask import g

conn = sqlite3.connect('database.db')
c = conn.cursor()


DATABASE = 'database.db'

#Create table


def get_db(): 
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = connect_to_database()
	return db

def connect_to_database():
	return sqlite3.connect('database.db')

def close_db():
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def add_user(email, password, firstname, familyname, gender, city, country):
	query_db('INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?)', [email, password, firstname, familyname, gender, city, country])
	return


def query_db(query, args=(), one=False):
	db=get_db()
	cur = db.execute(query, args)
	rv = cur.fetchall()
	print rv
	cur.close()
	db.commit()
	return (rv[0] if rv else None) if one else rv

def init_db(app):
	with app.app_context():
		db = get_db()
		with app.open_resource('database.schema', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()
