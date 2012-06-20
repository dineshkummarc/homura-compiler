import web

from app.models import Users


def user():
	user_id = int(web.cookies(user_id=0).get('user_id'))
	return Users.get(user_id)

def is_signed():
	return user() != None

def signin(user_id):
	web.setcookie('user_id', user_id, 600)

def signout():
	web.setcookie('user_id', 0, 0)


# using:
# @login_protected
# def GET(self, ...):
def login_protected(f):
	def decorated(*args, **kwargs):
		if not is_signed(): raise web.seeother('/signin')
		return f(*args, **kwargs)
	return decorated

# using:
# @admin_protected
# def GET(self, ...):
def admin_protected(f):
	def decorated(*args, **kwargs):
		if not is_signed(): raise web.seeother('/signin')
		if not user().is_admin: raise web.seeother('/signin')
		return f(*args, **kwargs)
	return decorated
