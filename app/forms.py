# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf          import FlaskForm
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField, IntegerField, HiddenField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired, Length, EqualTo, ValidationError
from app.models 		import Project

projects = Project.query.all()

class LoginForm(FlaskForm):
	username    = StringField  (u'Username'        , validators=[DataRequired()])
	password    = PasswordField(u'Password'        , validators=[DataRequired()])

class RegisterForm(FlaskForm):
	name        = StringField  (u'Name'      )
	username    = StringField  (u'Username'  , validators=[DataRequired()])
	password    = PasswordField(u'Password'  , validators=[DataRequired()])
	email       = StringField  (u'Email'     , validators=[DataRequired(), Email()])

class SupplyForm(FlaskForm):
	id		= HiddenField	('Id')
	name	= StringField	('Name', 	validators=[DataRequired()])
	brand	= StringField	('Brand', 	validators=[DataRequired()])
	stock	= IntegerField	('Stock', 	validators=[DataRequired()])
	submit	= SubmitField	('Submit')
	case 	= HiddenField	('Case',	validators=[DataRequired()])

class UsedSupplyForm(FlaskForm):
	supply_id	= HiddenField	('Supply_Id',	validators=[DataRequired()])
	#project_id	= IntegerField	('Project_Id',	validators=[DataRequired()])
	project_id	= SelectField	(choices = [(project.id, project.name) 	for project in projects],	validators=[DataRequired()])
	quantity	= IntegerField	('Quantity', 	validators=[DataRequired()])
	case 		= HiddenField	('Case',		validators=[DataRequired()])
	submit		= SubmitField	('Submit')
		