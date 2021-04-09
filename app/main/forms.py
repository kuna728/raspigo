from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, BooleanField, SelectMultipleField, FloatField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, Optional
from wtforms.widgets import TextArea, Select
from flask_wtf.file import FileField, FileRequired
from flask import Markup
from ..models import Category

class NewUserForm(FlaskForm):
	name = StringField('name')
	pictures = RadioField('Label', choices=['man1', 'man2', 'woman1', 'woman2'])
	submit = SubmitField('Utwórz')

class ConfigForm(FlaskForm):
	allowUsers = BooleanField()
	singleHomepage = BooleanField()
	mediaFolder = StringField()
	# allowAdminPassword = BooleanField()
	# adminPassword = PasswordField('New Password', validators=[
    #     Optional(), EqualTo('adminPasswordConfirm', message='Passwords must match')])
	# adminPasswordConfirm = PasswordField('Repeat Password', validators=[Optional()])
	minElPerSec = IntegerField()
	maxElPerSec = IntegerField()
	showEmpyCats = BooleanField()
	# colorSet = SelectField(choices=[(0, 'domyślny'), (1, 'ciemny'), (2, 'jasny')])
	submit1 = SubmitField('Zapisz i wróć')
	submit2 = SubmitField('Zapisz i zostań')

class SearchBarForm(FlaskForm):
	submit_value = Markup('<span class="fa fa-search"></span>')
	searchString = StringField()
	submit = SubmitField(submit_value)

class EditContentForm(FlaskForm):
	picture = FileField(validators=[Optional()])
	description = StringField(widget=TextArea())
	categories = SelectMultipleField(choices = [(str(i+1), Category.data[i]) for i in range(len(Category.data))], widget=Select(multiple=True))
	year = StringField()
	IMDBmark = FloatField()
	FWmark = FloatField()
	IMDBlink = StringField()
	FWlink = StringField()
	submit1 = SubmitField('Zapisz i wróć')
	submit2 = SubmitField('Zapisz i zostań')