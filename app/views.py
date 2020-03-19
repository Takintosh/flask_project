# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os, logging 

# Flask modules
from flask               import render_template, request, url_for, redirect, send_from_directory, flash
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort

# App modules
from app        import app, lm, db, bc
from app.models import User, Supply, FixedAsset, Student, Project, UsedSupply
from app.forms  import LoginForm, RegisterForm, SupplyForm, UsedSupplyForm

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET': 

        return render_template( 'pages/register.html', form=form, msg=msg )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:         

            pw_hash = password #bc.generate_password_hash(password)

            user = User(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    else:
        msg = 'Input error'     

    return render_template( 'pages/register.html', form=form, msg=msg )

# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            #if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"

    return render_template( 'pages/login.html', form=form, msg=msg ) 

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    content = None

    try:

        # @WIP to fix this
        # Temporary solution to solve the dependencies
        if path.endswith(('.png', '.svg' '.ttf', '.xml', '.ico', '.woff', '.woff2')):
            return send_from_directory(os.path.join(app.root_path, 'static'), path)    

        # try to match the pages defined in -> pages/<input file>
        return render_template( 'pages/'+path )

    except:
        
        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/404.html' ) )

# Vista de Insumos
@app.route('/insumos', methods=['GET', 'POST'])
def supplies():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    projects = Project.query.all()

    form                            = SupplyForm()
    usingform                       = UsedSupplyForm()
    usingform.project_id.choices    = [(project.id, project.name) 	for project in projects]

    if request.method == 'POST':

        # Agregar Insumo
        if form.case.data == "Agregar":
            if form.validate_on_submit():
                supply = Supply(name=form.name.data, brand=form.brand.data, stock=form.stock.data)
                
                db.session.add(supply)
                db.session.commit()
                flash('Insumo creado!', 'success')
                return redirect(url_for('supplies'))

        # Editar Insumo
        elif form.case.data == "Editar":
            if form.validate_on_submit():
                supply          = Supply.query.filter_by(id=form.id.data).first()
                supply.name     = form.name.data
                supply.brand    = form.brand.data
                supply.stock    = form.stock.data
                db.session.commit()
                flash('Insumo editado!', 'success')
                return redirect(url_for('supplies'))

        # Usar Insumo
        if usingform.case.data == "Usar":
            if usingform.validate_on_submit():

                quant = usingform.quantity.data
                for used in range(quant):
                    usedsupply = UsedSupply(project_id=usingform.project_id.data, supply_id=usingform.supply_id.data, authorized=current_user.id)
                    db.session.add(usedsupply)
                    db.session.commit()
                
                supply          = Supply.query.filter_by(id = usingform.supply_id.data).first()
                supply.stock    = supply.stock - usingform.quantity.data
                db.session.commit()
                
                flash('Insumo usado!', 'success')
                return redirect(url_for('supplies'))

    # Cargar Vista
    supplies    = Supply.query.all()
    return render_template('pages/insumos.html', supplies = supplies, form = form, usingform = usingform)


# Vista de Activos Fijos
@app.route('/activos')
def assets():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    assets = FixedAsset.query.all()
    return render_template('pages/activos.html', assets = assets)

# Vista de Usuarios
@app.route('/usuarios')
def users():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('pages/usuarios.html', users = users)

# Vista de Alumnos
@app.route('/alumnos')
def students():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    students = Student.query.all()
    return render_template('pages/estudiantes.html', students = students)

# Vista de Proyectos
@app.route('/proyectos')
def projects():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    projects = Project.query.all()
    return render_template('pages/proyectos.html', projects = projects)