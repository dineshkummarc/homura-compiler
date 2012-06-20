import web
from config import db
from collections import namedtuple

from app.helpers import utils



def check(username, password):
	r = db.select('users',
		vars = dict(username=username, password=password),
		what = '*',
		where = 'username=$username AND password=PASSWORD($password)',
		limit = 1)
	return len(r)==1
#

def make_user(r):
	r.is_admin = has_role(r.id, 'admin')
	return r

def get(id):
	r = db.select('users',
		vars = dict(id=id),
		what = '*',
		where = 'id=$id',
		limit = 1)
	if len(r) == 0: return None
	return make_user(r[0])
#

def get_by_username(username):
	r = db.select('users',
		vars = dict(username=username),
		what = '*',
		where = 'username=$username',
		limit =1 )
	if len(r) == 0: return None
	return make_user(r[0])
#

def get_roles(user_id):
	r = db.select('roles r, users_roles ur',
		vars = dict(user_id=user_id),
		what = 'r.id id, r.name name',
		where = 'r.id=ur.role_id AND ur.user_id=$user_id',
		limit = 100)
	return r

def has_role(user_id, role_name):
	r = db.select('users_roles ur, roles r',
		vars = dict(user_id=user_id, role_name=role_name),
		what = 'r.id',
		where = 'ur.role_id=r.id AND user_id=$user_id AND r.name=$role_name',
		limit = 1)
	return len(r) == 1
#

def get_role_by_name(name):
	r = db.select('roles',
		vars = dict(name=name),
		what = '*',
		where = 'name=$name',
		limit = 1)
	if len(r) != 1: return None
	return r[0]


def add(form):
	i = db.insert('users',
		username=form.username.value,
		password=web.SQLLiteral("PASSWORD('%s')" % form.password.value),
		created_at=web.SQLLiteral("NOW()"),
		firstname=form.firstname.value,
		lastname=form.lastname.value,
		isactive=1
	)
	db.insert('users_roles',
		user_id = i,
		role_id = get_role_by_name('login').id
	)
	return i
