import web, json
from config import view
from web import form

from app.helpers import render
from app.helpers import utils
from app.helpers import session

from app.models import Files


class Index:
	def GET(self):
		scripts = ['scripts/ace/ace.js',
			'scripts/ace/mode-csharp.js',
			'scripts/ace/mode-java.js',
			'scripts/ace/mode-c_cpp.js',
			'scripts/compiler.js',
			'scripts/jquery.easing.1.3.js',
			'scripts/jqueryFileTree.js']
		styles = ['css/jqueryFileTree.css',]
		return render.layout(view.index(issigned=session.is_signed()), title='Home', scripts=scripts, styles=styles)


class Sample:
	def GET(self):
		return render.layout(view.sample(), title='Sample')


class About:
	def GET(self):
		return render.layout(view.about(), title='About')


class Return:
	def POST(self):
		x = web.input(source_file={})['source_file'].value
		web.header('Content-type', 'text/plain')
		return x
# end Return


class Directory:
	def TEMP(self):
		web.header('Content-type', 'text/html')
		user_id = session.user().id
		dir_ = web.input(dir='/')['dir']
		parent_id = dir_.split('/')
		parent_id = parent_id[-2] if len(parent_id[-1]) == 0 else parent_id[-1]
		if len(parent_id)==0: parent_id = None
		dirs = Files.get_directories(user_id, parent_id)
		files = Files.get_files(user_id, parent_id)
		s = ['<ul class="jqueryFileTree" style="display: none;">']
		if dir_[-1] != '/': dir_+='/'
		for d in dirs:
			s.append('<li class="directory collapsed"><a href="#" rel="%s%d/">%s</a></li>' % (dir_, d.id, d.name))
		for f in files:
			s.append('<li class="file ext_txt"><a href="#" rel="%s%d">%s</a></li>' % (dir_, f.id, f.name))
		s.append('</ul>')
		return ' '.join(s)

	def POST(self):
		return self.TEMP()
	
	def GET(self):
		return self.TEMP()
#end File

class File:
	def TEMP(self):
		web.header('Content-type', 'text/plain')
		user_id = session.user().id
		f = web.input(file=None)['file'].split('/')
		f = f[-2] if len(f[-1]) == 0 else f[-1]
		if len(f)==0: f = None
		f = Files.get_file(f)
		return json.dumps({'name': f.name, 'body': f.body, 'id': f.id})

	def POST(self):
		return self.TEMP()
	
	def GET(self):
		return self.TEMP()
#end File

class Save:
	def POST(self):
		web.header('Content-type', 'text/plain')
		
		user_id = session.user().id

		sid = int(web.input(id='0')['id'], 10)
		sname = web.input(name='')['name']
		scode = web.input(code='')['code']

		return Files.save(user_id, sid, sname, scode)
