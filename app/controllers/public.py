import web
import mimetypes

public_dir = 'public'

class Public:
	def GET(self):
		try:
			filename = web.ctx.path.split('/')[-1]
			web.header('Content-type', mime_type(filename))
			#web.header('Content-type','text/html')
			#web.header('Transfer-Encoding','chunked') 
			#print 'Content-type - ', mime_type(filename)
			return open(public_dir + web.ctx.path, 'rb').read()
		except IOError:
			raise web.notfound()


def mime_type(filename):
	return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
