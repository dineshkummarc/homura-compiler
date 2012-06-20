import web
from config import view

from app.helpers import utils
from app.helpers import session

def layout(page, title, **args):
	title = ('Compiler at KBTU', 'Compiler - '+title)[len(title)>0]
	user = session.user()
	return view.layout(page, user=user, title=title, **args)
