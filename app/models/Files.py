import web
from config import db
from collections import namedtuple

from app.helpers import utils


def get_directories(user_id, parent_id=None, limit = 50):
	return db.select('directories',
		vars=dict(user_id=user_id, parent_id=parent_id),
		what='id, user_id, name, parent_id, created_date, updated_date',
		where='user_id=$user_id AND parent_id %s $parent_id' % ('=','is')[parent_id is None],
		order='name',
		limit = limit)

def get_files(user_id, parent_id=None, limit = 50):
	return db.select('files',
		vars=dict(user_id=user_id, parent_id=parent_id),
		what='id, user_id, name, parent_id, created_date, updated_date',
		where='user_id=$user_id AND parent_id %s $parent_id' % ('=','is')[parent_id is None],
		order='name',
		limit = limit)

def get_file(file_id):
	r = db.select('files',
		vars=dict(file_id=file_id),
		what='id, user_id, name, body, parent_id, created_date, updated_date',
		where='id=$file_id',
		limit = 1)
	return (None, r[0])[len(r)==1]

def save(user_id, file_id, name, body, parent_id=None):
	if file_id == 0:
		result = 0
		try:
			result = db.insert('files', user_id=user_id, name=name, body=body, parent_id=parent_id, created_date=web.SQLLiteral('NOW()'))
		except Exception as inst:
			pass
		return result
	else:
		# check has user_id file file_id
		r = db.select('files',
			vars=dict(user_id=user_id, id=file_id),
			what='id',
			where='user_id=$user_id AND id=$id',
			limit=1)
		if len(r) == 1:
			return db.update('files', vars=dict(id=file_id), name=name, body=body, parent_id=parent_id, where='id=$id')
