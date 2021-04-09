import os
import json
from flask import current_app
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = 'ljo1u0jni12j 98udjakslmdajSDH912HD12 NDL1KWD'
	SQLALCHEMY_DATABASE_URI =  'sqlite:///' + os.path.join(basedir, 'data.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MEDIA_FOLDER = '/media/pi/<dysk>/raspigo'
	ALLOW_USERS = False
	# USE_ADMIN_PASSWORD = False
	# ADMIN_PASSWORD = ''
	SINGLE_HOMEPAGE = False
	ELEMENTS_PER_SECTION_MIN = 1
	ELEMENTS_PER_SECTION_MAX = 20
	COLOR_SET = 0
	SHOW_EMPTY_CATEGORIES = True

	@staticmethod
	def Save():
		with open('config.json', 'w') as f:
			json.dump({ a:Config.__dict__[a] for a in Config.__dict__ if a[:2]!='__' and a not in ('Save', 'Load', 'SQLALCHEMY_DATABASE_URI')}, f)
	@staticmethod
	def Load():
		with open('config.json', 'r') as f:
			d = json.load(f)
			for c in d.keys():
				setattr(Config, c, d[c])