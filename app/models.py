from . import db
from datetime import datetime

MovieCategory = db.Table('movie_category', 
	db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
	db.Column('category_id', db.Integer, db.ForeignKey('categories.id')))

SeriesCategory = db.Table('series_category', 
	db.Column('series_id', db.Integer, db.ForeignKey('series.id')),
	db.Column('category_id', db.Integer, db.ForeignKey('categories.id')))

UserCategory = db.Table('user_category',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('category_id', db.Integer, db.ForeignKey('categories.id')))


class UserMovie(db.Model):
	__tablename__='user_movie'
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
	watching_datetime = db.Column(db.DateTime, default=datetime.now())
	watched_time = db.Column(db.Integer, default=0)
	video_duration = db.Column(db.Integer)
	movies = db.relationship("Movie")

class UserSeries(db.Model):
	__tablename__='user_series'
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	seasons_id = db.Column(db.Integer, db.ForeignKey('series.id'), primary_key=True)
	watching_datetime = db.Column(db.DateTime, default=datetime.now())
	watched_time = db.Column(db.Integer, default=0)
	video_duration = db.Column(db.Integer)
	season = db.Column(db.Integer)
	episode = db.Column(db.Integer)
	series = db.relationship("Series")

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	picture = db.Column(db.String(10))
	enabled = db.Column(db.Boolean())
	cats = db.relationship('Category', secondary=UserCategory, 
		backref=db.backref('User'))
	movies = db.relationship('UserMovie',)
	series = db.relationship('UserSeries')

	def __repr__(self):
		return '<User %r>' % self.username

class Category(db.Model):
	data = ['Komedia', 'Horror', 'Thriller', 'Komedia rom.', 'Animacja', 'Wojenny',
					'Sci-Fi', 'Akcja', 'Dla młodzieży', 'Kryminał', 'Fantasy',
					'Anime', 'Biograficzny', 'Czarna komedia',
					'Dla dzieci', 'Dokumentalny', 'Dramat', 'Dramat obyczajowy',
					'Dramat sądowy', 'Dramat społeczny', 'Dreszczowiec', 'Familijny', 'Gangsterski',
					'Katastroficzny', 'Komedia obycz.', 'Krótkometrażowy', 'Melodramat', 'Musical',
					'Obyczajowy', 'Polityczny', 'Przygodowy', 'Przyrodniczy', 'Psychologiczny', 'Inne']
	__tablename__ = 'categories'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(40), unique=True, nullable=False)


class Movie(db.Model):
	__tablename__ = 'movies'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False, unique=True)
	added = db.Column(db.DateTime, nullable=False)
	img = db.Column(db.String(30))
	year = db.Column(db.String(11))
	cats = db.relationship('Category', secondary=MovieCategory, 
		backref=db.backref('Movies'))
	description = db.Column(db.String(300))
	FWmark = db.Column(db.String(5))
	IMDBmark = db.Column(db.String(5))
	FWlink = db.Column(db.String(100))
	IMDBlink = db.Column(db.String(100))

class Series(db.Model):
	__tablename__ = 'series'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False, unique=True)
	added = db.Column(db.DateTime, nullable=False)
	img = db.Column(db.String(30))
	year = db.Column(db.String(11))
	cats = db.relationship('Category', secondary=SeriesCategory, 
		backref=db.backref('Series'))
	description = db.Column(db.String(300))
	FWmark = db.Column(db.String(5))
	IMDBmark = db.Column(db.String(5))
	FWlink = db.Column(db.String(100))
	IMDBlink = db.Column(db.String(100))
	seasons = db.relationship('Seasons', backref='series')

class Seasons(db.Model):
	__tablename__ = 'seasons'
	id = db.Column(db.Integer, primary_key=True)
	series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
	season = db.Column(db.Integer)
	episodes = db.Column(db.Integer)


class Section():
	def __init__(self, title, elements):
		self.title = title
		self.elements = elements 