import web
from config import view
from web import form
import json, re

from app.helpers import render, utils, session

from app.models import Users

val_username	= form.regexp(r'^\w[\w\d_]{2,19}$', 'must be betweem 3 and 20 characters. username should containt only latin alphabet, digits and underscores')
val_password	= form.regexp(r'^.{3,}$', 'must have more than 3 characters')
val_email		= form.regexp(r'^.+@.+$', 'must be a valid email address')

LoginForm = form.Form(
	form.Textbox('username', val_username, description='Username'),
	form.Password('password',val_password, description='Password'),	
	form.Button('submit', type='submit', html='Sign in'),
	validators = [
		form.Validator("Username or Password is incorrect", lambda i: Users.check(i.username, i.password)),
	]
)

class Signin:
	def __makepage(self, loginform = None):
		if loginform is None: loginform = LoginForm()
		return render.layout(view.signin(loginform), title="Sign in")

	def GET(self):
		return self.__makepage()

	def POST(self):
		loginform = LoginForm()
		if not loginform.validates():
			return self.__makepage(loginform)
		user = Users.get_by_username(loginform.username.value)
		session.signin(user.id)
		return web.seeother('/')
# end Login


class Signout:
	def GET(self):
		session.signout()
		return web.seeother('/')


RegForm = form.Form(
	form.Textbox('username', val_username, description='Username'),
	form.Password('password',val_password, description='Password'),
	form.Password('password2',val_password, description='Password again'),
	form.Textbox('firstname', description='First name'),
	form.Textbox('lastname', description='Last name'),
	form.Button('submit', type='submit', html='Sign up'),
	validators = [
		form.Validator("Username or Password is incorrect", lambda i: i.password == i.password2),
		form.Validator("Username is already taken", lambda i: not Users.get_by_username(i.username)),
	]
)

class Signup:
	def __makepage(self, regform = None):
		if regform is None: regform = RegForm()
		return render.layout(view.signup(regform), title="Sign up")

	def GET(self):
		return self.__makepage()

	def POST(self):
		regform = RegForm()
		if not regform.validates():
			return self.__makepage(regform)
		Users.add(regform)
		return web.seeother('/signin')
# end Login

