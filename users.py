from flask import Flask, make_response, request, render_template, redirect, url_for, session, send_file, after_this_request
from werkzeug.utils import secure_filename

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'Verysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////C:\Users\tcmvd\renam>'

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50) ])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)



@app.route('/')
def home():
 if not session.get('logged_in'):
  return render_template('login.html')
 else:
  return "Hello Boss!"


# @app.route('/login', methods=['POST'])
# def do_admin_login():
#  if request.form['password'] == 'password' and request.form['username'] == 'admin':
#   session['logged_in'] = True
#  else:
#   flash('wrong password!')
#   return home()
