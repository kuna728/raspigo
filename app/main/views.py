from flask import Flask, render_template, redirect, url_for, send_from_directory, current_app, session, abort, request, flash
from .. import db
from ..models import User, Movie, Series, Category, Seasons, Section, UserMovie, UserSeries
from . import main
from .forms import NewUserForm, ConfigForm, SearchBarForm, EditContentForm
import os
import sys
import re
from config import Config
from datetime import datetime
from werkzeug.datastructures import MultiDict
from werkzeug.utils import secure_filename

@main.before_request
def before_request():
	if not current_app.config['ALLOW_USERS']:
		session['current_user'] = 1
	
	if (session.get('current_user', None) and session['current_user']==1 and current_app.config['ALLOW_USERS'] 
		and request.path not in ('/', '/config/') and not re.findall('/userlogin/[0-9]', request.path)):
		flash('Wybierz konto użytkownika lub je wyłącz aby kontynuować')
		return redirect(url_for('.index'))


@main.route('/', methods=['GET', 'POST'])
def index():
	if not current_app.config['ALLOW_USERS']:
		return redirect(url_for('.home'))
	form = NewUserForm()
	users = User.query.all()
	if form.validate_on_submit():
		user = User(username=form.name.data, picture=form.pictures.data, enabled=True)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('.index'))

	return render_template('profile.html', form=form, users=users[1:])

@main.route('/userlogin/<id>')
def user_login(id):
	user = User.query.filter_by(id=id).first()
	if not user:
		abort(404)
	session['current_user'] = id
	return redirect(url_for('.home'))

@main.route('/config/', methods=['GET', 'POST'])
def config():
	form = ConfigForm()
	if request.method == 'POST':
		form=ConfigForm()
	else:
		form = ConfigForm(formdata=MultiDict(
			{'allowUsers': Config.ALLOW_USERS,
			 'mediaFolder' : Config.MEDIA_FOLDER,
			'singleHomepage': Config.SINGLE_HOMEPAGE,
			'minElPerSec': Config.ELEMENTS_PER_SECTION_MIN,
			'maxElPerSec': Config.ELEMENTS_PER_SECTION_MAX,
			'showEmpyCats': Config.SHOW_EMPTY_CATEGORIES}))
	users = User.query.all()
	content = Movie.query.all()[:20] + Series.query.all()[:20]
	content.sort(reverse=True, key=(lambda x : x.added))
	if form.validate_on_submit():
		current_app.config['ALLOW_USERS'] = Config.ALLOW_USERS = form.allowUsers.data
		current_app.config['MEDIA_FOLDER'] = Config.MEDIA_FOLDER = form.mediaFolder.data
		current_app.config['SINGLE_HOMEPAGE'] = Config.SINGLE_HOMEPAGE = form.singleHomepage.data
		current_app.config['ELEMENTS_PER_SECTION_MIN'] = Config.ELEMENTS_PER_SECTION_MIN = form.minElPerSec.data
		current_app.config['ELEMENTS_PER_SECTION_MAX'] = Config.ELEMENTS_PER_SECTION_MAX = form.maxElPerSec.data
		current_app.config['SHOW_EMPTY_CATEGORIES'] = Config.SHOW_EMPTY_CATEGORIES = form.showEmpyCats.data 
		Config.Save()
		if request.cookies.get("redirect")=="False":
			return redirect(url_for('.config'))
		else:
			return redirect(url_for('.index'))
		
	return render_template('config.html', form=form, users=users[1:], content=content[:20])

@main.route('/editcontent/<tp>_<id>/', methods=['GET', 'POST'])
def config_content(tp, id):
	if tp=='s':
		content = Series.query.filter_by(id=id).first()
	else:
		content = Movie.query.filter_by(id=id).first()
	if request.method == 'POST':
		form=EditContentForm()
	else:
		form = EditContentForm(formdata=MultiDict(
			{'description': content.description,
			'categories': [cat.id for cat in content.cats],
			'year': content.year,
			'IMDBmark': content.IMDBmark,
			'FWmark': content.FWmark.replace(',', '.'),
			'IMDBlink': content.IMDBlink,
			'FWlink': content.FWlink}))
	if form.validate_on_submit():
		content.description = form.description.data
		content.year = form.year.data
		content.IMDBmark = form.IMDBmark.data
		content.IMDBlink = form.IMDBlink.data
		content.FWmark = form.FWmark.data
		content.FWlink = form.FWlink.data
		if form.categories.data != [cat.id for cat in content.cats]:
			content.cats = []
			for cat in form.categories.data:
				content.cats.append(Category.query.filter_by(id=int(cat)).first())
		db.session.commit()
		if form.picture.data:
			form.picture.data.save(current_app.config['MEDIA_FOLDER']+'/' + content.__tablename__ + '/' + content.title + '/desktop.png')
		if request.cookies.get("redirect")=="False":
			return redirect(url_for('.config_content', tp=tp, id=id))
		else:
			return redirect(url_for('.config'))
	return render_template('edit.html',form=form, content=content)

@main.route('/personalization', methods=['GET', 'POST'])
def user_config():
	form = NewUserForm()
	user = User.query.filter_by(id=session['current_user']).first()
	if form.validate_on_submit():
		user.username = form.name.data
		user.picture = form.pictures.data
		db.session.commit()
	content = []
	if user.movies or user.series:
		elements = user.movies + user.series
		elements.sort(reverse=True, key=(lambda x : x.watching_datetime))
		for element in elements:
			if isinstance(element, UserMovie):
				element.movies.titleAddition = ''
				element.movies.watching_datetime = element.watching_datetime
				element.movies.watched_time = '%.2i:%.2i:%.2i' % (element.watched_time/3600, (element.watched_time%3600)/60, element.watched_time%60)
				content.append(element.movies)
			else:
				element.series.titleAddition = ' S%.2iE%.2i' % (element.season, element.episode)
				element.series.watching_datetime = element.watching_datetime
				element.series.watched_time = '%.2i:%.2i:%.2i' % (element.watched_time/3600, (element.watched_time%3600)/60, element.watched_time%60)
				content.append(element.series)
	return render_template('personalization.html', form=form, categories=user.cats, content=content)

@main.route('/home/')
def home():
	if request.form.get('registration') == 'success':
		return json.dump({"abc":'successfuly registered'})
	if current_app.config['SINGLE_HOMEPAGE']:
		return redirect(url_for('.show_list'))
	user = User.query.filter_by(id=session['current_user']).first()
	sections = []
	if user.movies or user.series:
		elements = user.movies + user.series
		elements.sort(reverse=True, key=(lambda x : x.watching_datetime))
		sec_elements = []
		print(elements,file=sys.stderr)
		for element in elements:
			if isinstance(element, UserMovie):
				element.movies.titleAddition = ''
				element.movies.watched_percent = element.watched_time / element.video_duration * 100
				sec_elements.append(element.movies)
			else:
				element.series.titleAddition = ' S%.2iE%.2i' % (element.season, element.episode)
				element.series.watched_percent = element.watched_time / element.video_duration * 100
				sec_elements.append(element.series)
		sections.append(Section('Ostatnio oglądane', sec_elements))
	if len(Movie.query.all()+Series.query.all()) <= current_app.config['ELEMENTS_PER_SECTION_MAX']:
		sections.append(Section('Wszystkie', Movie.query.all() + Series.query.all()))
	for cat in user.cats:
		sections.append(Section(cat.name, cat.Movies+cat.Series))
	if (len(Movie.query.all()) >= current_app.config['ELEMENTS_PER_SECTION_MIN']
		and len(Movie.query.all()) <= current_app.config['ELEMENTS_PER_SECTION_MAX']):
		sections.append(Section('Filmy', Movie.query.all()))
	if (len(Series.query.all()) >= current_app.config['ELEMENTS_PER_SECTION_MIN']
		and len(Series.query.all()) <= current_app.config['ELEMENTS_PER_SECTION_MAX']):
		sections.append(Section('Seriale', Series.query.all()))
	categories = Category.query.all()
	categories.sort(reverse=True, key=(lambda x : len(x.Series+x.Movies)))
	for cat in categories:
		if (cat not in user.cats 
			and (len(cat.Series + cat.Movies)) >= current_app.config['ELEMENTS_PER_SECTION_MIN']
			and (len(cat.Series + cat.Movies)) <= current_app.config['ELEMENTS_PER_SECTION_MAX']):
			sections.append(Section(cat.name, cat.Movies+cat.Series))
	
	return render_template('home.html', allowUsers=current_app.config['ALLOW_USERS'], sections=sections)

@main.route('/play/<tp>_<id>/')
@main.route('/play/<tp>_<id>_<se>/')
def play(tp, id, se=None):
	user = User.query.filter_by(id=session['current_user']).first()
	s, e, _s, _e, we = None, None, None, None, 0
	if tp=='s':
		content = Series.query.filter_by(id=id).first()
		userseriesEl = [s for s in user.series if s.series==content]
		if userseriesEl:
			_s, _e = userseriesEl[0].season, userseriesEl[0].episode
			if not se:
				we = userseriesEl[0].watched_time		
		if se==None:
			if _s and _e:
				s, e = _s, _e
			else:
				s, e = 1, 1
		else:
			s, e  = int(se[1:3]), int(se[4:6])
		videoUrl = content.__tablename__+'/'+content.title+'/S{}/E{}'.format(s,e)
		ls = os.listdir(current_app.config['MEDIA_FOLDER']+'/'+videoUrl)
	elif tp=='m':
		content = Movie.query.filter_by(id=id).first()
		usermovieEl = [m for m in user.movies if m.movies==content]
		if usermovieEl:
			we = usermovieEl[0].watched_time
		videoUrl = content.__tablename__+'/'+content.title
		ls = os.listdir(current_app.config['MEDIA_FOLDER']+'/'+videoUrl)
	subtitles = [el[:-4] for el in ls if el.endswith('.vtt')]
	videoUrl += '/'+[el for el in ls if not el.endswith(('.vtt', '.srt', '.jpg', '.jpeg', '.png', 'gif'))][0]
	return render_template('play.html', videoUrl=videoUrl, content=content, season_episode=(s, e), watched_time=we, subtitles=subtitles)

@main.route('/enableuser/<id>/')
def enableUser(id):
	user = User.query.filter_by(id=id).first()
	if user:
		user.enabled = not user.enabled
		db.session.commit()
	return redirect(url_for('.config'))

@main.route('/deleteuser/<id>/')
def deleteUser(id):
	user = User.query.filter_by(id=id).first()
	if user:
		User.query.filter_by(id=id).delete()
		db.session.commit()
	return redirect(url_for('.config'))

@main.route('/deletelastwatched/<tp>_<id>')
@main.route('/deletelastwatched/<tp>_<id>_<rd>')
def delete_last_watched(tp, id, rd=None):
	user = User.query.filter_by(id=session['current_user']).first()
	if tp=='s':
		UserSeries.query.filter_by(user_id=user.id, seasons_id = id).delete()
	else:
		UserMovie.query.filter_by(movie_id=id, user_id=user.id).delete()
	db.session.commit()
	if rd:
		return redirect(url_for('.user_config'))
	return redirect(url_for('.show_list', string='ostatnio oglądane'))

@main.route('/forceupdate/')
@main.route('/forceupdate/<ac>/<tp>_<id>/')
def force_update(ac=None, tp=None, id=None):
	if ac==None:
		from ..scripts.scan import Main
		log = Main()
		added_movies = ', '.join(log[0][0]) if log[0][0] else None
		removed_movies = ', '.join(log[0][1]) if log[0][1] else None
		added_series = ', '.join(log[1][0]) if log[1][0] else None
		removed_series = ', '.join(log[1][1]) if log[1][1] else None
		if added_movies:
			flash('Dodane filmy: %s.' % added_movies, 'alert-success')
		if added_series: 
			flash('Dodane seriale: %s.' % added_series, 'alert-success')
		if removed_movies:
			flash('Usunięte filmy: %s.' % removed_movies, 'alert-danger')
		if removed_series:
			flash('Usunięte seriale: %s.' % removed_series, 'alert-danger')
		if not added_movies and not added_series and not removed_movies and not removed_series:
			flash('Nie wykryto żadnych zmian w katalogu aplikacji: %s' % Config.MEDIA_FOLDER, 'alert-warning')
		return redirect(url_for('.config'))
	else:
		from ..scripts.scrap import GetInfo
		if tp=='s':
			content = Series.query.filter_by(id=id).first()
		else:
			content = Movie.query.filter_by(id=id).first()
		if ac=='picture':
			from ..scripts.googleImg import DownloadImg
			DownloadImg(tags=[content.title], dir=current_app.config['MEDIA_FOLDER']+'/'+content.__tablename__)
		elif ac=='filmweb':
			result = GetInfo(fwlink=content.FWlink)
			content.FWmark = result[0]
			content.cats = []
			if type(result[1]) is list:
				for c in result[1]:
					cat = Category.query.filter_by(name=c).first()
					if cat:
						content.cats.append(cat)
			else:
				cat = Category.query.filter_by(name=result[1]).first()
				if cat:
					content.cats.append(cat)
			content.year = result[2]
			content.description = result[3]
			db.session.commit()
		elif ac=='imdb':
			result = GetInfo(imdblink=content.IMDBlink)
			content.IMDBmark = result[0]
			db.session.commit()
		else:
			abort(404)
		return redirect(url_for('.config_content', tp=tp, id=id))

@main.route('/list/', methods=['GET', 'POST'])
@main.route('/list/<string>', methods=['GET', 'POST'])
def show_list(string=None):
	form = SearchBarForm()
	if form.validate_on_submit():
		search = "%{}%".format(form.searchString.data)
		content = Movie.query.filter(Movie.title.like(search)).all() + Series.query.filter(Series.title.like(search)).all() 	
	else:
		content = []
		if string=='ostatnio oglądane':
			user = User.query.filter_by(id=session['current_user']).first()
			elements = user.movies + user.series
			elements.sort(reverse=True, key=(lambda x : x.watching_datetime))
			for element in elements:
				if isinstance(element, UserMovie):
					content.append(element.movies)
				else:
					content.append(element.series)
		
		if string=='seriale' or string=='wszystkie' or string==None:
			content.extend(Series.query.all())
		if string=='filmy' or string=='wszystkie' or string==None:
			content.extend(Movie.query.all())
		try:
			cat = Category.query.filter_by(name=string.capitalize()).first()
			content.extend(cat.Movies)
			content.extend(cat.Series)
		except AttributeError:
			pass
	return render_template('list.html', allowUsers=current_app.config['ALLOW_USERS'],title=string if string!='search' else form.searchString.data, content = content)

@main.route('/saveprogress/<tp>_<id>/<_s>_<_e>/<t>/')
@main.route('/saveprogress/<tp>_<id>/<_s>_<_e>/')
@main.route('/saveprogress/<tp>_<id>/<t>/')
@main.route('/saveprogress/<tp>_<id>/')
def save_progress(tp, id, _s=None, _e=None, t=None):
	user = User.query.filter_by(id=session['current_user']).first()
	watched_time, video_duration =  map(int, map(float, request.url.split('/')[-2].split(':')))
	if tp=='s':
		content = Series.query.filter_by(id=id).first()
		userseriesEl = [s for s in user.series if s.series==content]
		temp = UserSeries()
		if userseriesEl:		
			db.session.delete(userseriesEl[0])
			db.session.commit()
		s, e = temp.season, temp.episode = int(_s), int(_e)
		temp.series = content
		temp.watching_datetime = datetime.now()
		temp.watched_time = watched_time
		temp.video_duration = video_duration
		user.series.append(temp)
		db.session.commit()
	elif tp=='m':
		content = Movie.query.filter_by(id=id).first()
		usermovieEl = [m for m in user.movies if m.movies==content]
		if usermovieEl:
			db.session.delete(usermovieEl[0])
			db.session.commit()			
		temp = UserMovie()
		temp.movies = content
		temp.watching_datetime = datetime.now()
		temp.watched_time = watched_time
		temp.video_duration = video_duration
		user.movies.append(temp)
		db.session.commit()
	return ''

@main.route('/categories/')
def list_categories():
	user = User.query.filter_by(id=session['current_user']).first()
	categories = Category.query.all()
	if not categories:
		return render_template('cat.html', categories=[])
	for c in Category.query.all():
		if(not current_app.config['SHOW_EMPTY_CATEGORIES'] and not c.Movies and not c.Series):
			categories.remove(c)
		if c in user.cats:
			c.followed = True
		else:
			c.followed = False
		c.count = len(c.Movies + c.Series)
	categories.sort(reverse=True, key=(lambda x : x.count))
	return render_template('cat.html', categories=categories)

@main.route('/followcategory/<id>')
@main.route('/followcategory/<id>_<rd>')
def follow_category(id, rd=None):
	user = User.query.filter_by(id=session['current_user']).first()
	cat = Category.query.filter_by(id=id).first()
	if cat in user.cats:
		user.cats.remove(cat)
	else:
		user.cats.append(cat)
	db.session.commit()
	if rd:
		return redirect(url_for('.user_config'))
	return redirect(url_for('.list_categories'))


@main.route('/uploads/<path:filename>')
def download_file(filename):
	if os.path.isfile(current_app.config['MEDIA_FOLDER']+'/' + filename):
		return send_from_directory(current_app.config['MEDIA_FOLDER'], filename, as_attachment=True)
	else:
		return redirect(url_for('static', filename='img/default.png'))