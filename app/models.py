# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app         import db
from flask_login import UserMixin


# Modelo Usuario
class User(UserMixin, db.Model):

    id       = db.Column(db.Integer,     primary_key = True)
    user     = db.Column(db.String(64),  unique = True)
    email    = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(500))

    def __init__(self, user, email, password):
        self.user       = user
        self.password   = password
        self.email      = email

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.user)

    def save(self):
        db.session.add ( self )
        db.session.commit( )
        return self 

# Modelo Insumos
class Supply(db.Model):
    id          = db.Column(db.Integer,         primary_key = True)
    name        = db.Column(db.String(64),      unique = True)
    brand       = db.Column(db.String(64))
    stock       = db.Column(db.Integer)
    supplies    = db.relationship('UsedSupply', backref='fromSupply')

# Modelo Estudiante
class Student(db.Model):
    id          = db.Column(db.Integer,         primary_key = True)
    name        = db.Column(db.String(64))
    surname     = db.Column(db.String(64))
    enrollment  = db.Column(db.String(64))
    projects    = db.relationship('Project',    backref='owner')

# Modelo Proyecto
class Project(db.Model):
    id          = db.Column(db.Integer,         primary_key = True)
    name        = db.Column(db.String(64))
    student_id  = db.Column(db.Integer,         db.ForeignKey('student.id'))
    supply_id   = db.relationship('UsedSupply', backref='usingSupply')
    
# Modelo Insumo Usado
class UsedSupply(db.Model):
    id          = db.Column(db.Integer,     primary_key = True)
    supply_id   = db.Column(db.Integer,     db.ForeignKey('supply.id'))
    project_id  = db.Column(db.Integer,     db.ForeignKey('project.id'))
