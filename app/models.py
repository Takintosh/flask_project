# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app         import db
from flask_login import UserMixin


# Clase Usuario
class User(UserMixin, db.Model):

    id      = db.Column(db.Integer,     primary_key = True)
    user    = db.Column(db.String(64),  unique = True)
    name    = db.Column(db.String(64),  unique = False)
    surname = db.Column(db.String(64),  unique = False)
    email   = db.Column(db.String(120), unique = True)
    rank    = db.Column(db.String(120), unique = False)
    password = db.Column(db.String(500))

    def __init__(self, user, email, password):
        self.user       = user
        self.name       = name
        self.surname    = surname
        self.password   = password
        self.email      = email
        self.rank       = rank

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.user)

    def save(self):
        db.session.add ( self )
        db.session.commit( )
        return self 

# Clase Insumos
class Supply(db.Model):
    id          = db.Column(db.Integer,         primary_key = True)
    name        = db.Column(db.String(64),      unique = True)
    brand       = db.Column(db.String(64))
    stock       = db.Column(db.Integer)
    usedsupplies    = db.relationship("UsedSupply", backref="supply")

    def __init__(self, name, brand, stock):
        self.name   = name
        self.brand  = brand
        self.stock  = stock


# Clase Estudiante
class Student(db.Model):
    id          = db.Column(db.Integer,         primary_key = True)
    name        = db.Column(db.String(64))
    surname     = db.Column(db.String(64))
    enrollment  = db.Column(db.String(64))
    
    def __init__(self, name, surname, enrollment):
        self.name       = name
        self.surname    = surname
        self.enrollment = enrollment

# Clase Proyecto
class Project(db.Model):
    id          = db.Column(db.Integer,         primary_key = True)
    name        = db.Column(db.String(64))
    student_id  = db.Column(db.Integer,         db.ForeignKey('student.id'),    nullable=False)
    student     = db.relationship("Student",    backref="owner", uselist=False, foreign_keys=[student_id])

    user_id     = db.Column(db.Integer,         db.ForeignKey('user.id'),       nullable=False)
    professor   = db.relationship("User",       backref="incharge", uselist=False,  foreign_keys=[user_id])
    
    supply_id   = db.relationship('UsedSupply', backref='usingSupply')

    def __init__(self, name):
        self.name       = name
    
# Clase Insumo Usado
class UsedSupply(db.Model):
    id              = db.Column(db.Integer,     primary_key = True)
    supply_id       = db.Column(db.Integer,     db.ForeignKey('supply.id'),     nullable=False)
    project_id      = db.Column(db.Integer,     db.ForeignKey('project.id'),    nullable=False)
    authorized      = db.Column(db.Integer,     db.ForeignKey('user.id'),       nullable=False)

# Clase Sala
class Room(db.Model):
    id      = db.Column(db.Integer,         primary_key = True)
    name    = db.Column(db.String(64))

    def __init__(self, name):
        self.name   = name

# Clase Activos Fijos
class FixedAsset(db.Model):
    id              = db.Column(db.Integer,     primary_key = True)
    name            = db.Column(db.String(64))
    status          = db.Column(db.String(64))
    originroom_id   = db.Column(db.Integer,     db.ForeignKey(Room.id),   nullable=True)
    actualroom_id   = db.Column(db.Integer,     db.ForeignKey(Room.id),   nullable=True)
    originroom      = db.relationship("Room", backref="originroom", uselist=False, foreign_keys=[originroom_id])
    actualroom      = db.relationship("Room", backref="actualroom", uselist=False, foreign_keys=[actualroom_id])

    def __init__(self, name, status):
        self.name   = name
        self.status = status