import web
from config import db
from collections import namedtuple

from app.helpers import utils

from app.models import threads


def get_boards(limit = 10):
	return db.select('boards',
		what='id, shortname, name, description',
		order='id',
		limit = limit)


def get_board(board_id):
	b = db.select('boards',
		vars=dict(board_id=board_id),
		what='*',
		where='id=$board_id',
		limit=1)
	return (None, b[0])[len(b)==1]

def get_board_byshortname(shortname):
	b = db.select('boards',
		vars=dict(shortname=shortname),
		what='*',
		where='shortname=$shortname',
		limit=1)
	return (b[0], None)[len(b)!=1]


def get_board_threads(board_id, limit = 10):
	return db.select('threads',
		vars=dict(board_id=board_id),
		what='id, image, text, title, created_at',
		order='updated_at DESC',
		where='board_id=$board_id',
		limit = limit)

		
def get_board_threads_with_posts(board_id, limit = 10, postlimit = 4):
	tps = []
	for thread in get_board_threads(board_id, limit):
		tps.append(threads.get_thread_with_posts(thread.id, postlimit))
	return tps
