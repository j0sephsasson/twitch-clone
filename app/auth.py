from flask import Blueprint, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask.templating import render_template
from .db_models import User, Img
from . import db
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

## endpoint to signup users
@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    pic = request.files['pic'] ## get uploaded pic

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user for the user table. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # create a new user for the image table
    filename = secure_filename(pic.filename) ## hash filename
    mimetype = pic.mimetype ## get file type
    if not filename or not mimetype:
        return 'Bad upload!', 400
    img = Img(img=pic.read(), name=filename, mimetype=mimetype, email = email)

    # add the new user to the database
    db.session.add(new_user)
    db.session.add(img)
    db.session.commit()

    flash('Success! Account Created.')  ## successful signup alert

    return render_template('signup.html')

## endpoint to login users
@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page w/ flash

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))