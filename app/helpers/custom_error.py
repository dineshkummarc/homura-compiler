import web

from app.helpers import render
from config import view

def notfound():
	return web.notfound(render.layout(view.not_found(), title='File not found', mode='error404'))

def add(app):
	app.internalerror = web.debugerror
	app.notfound = notfound
	#app.internalerror = web.config.debug and web.debugerror or internalerror
