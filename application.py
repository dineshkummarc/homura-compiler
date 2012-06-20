# abspath, and other 2 lines need for apache server

import sys, os
#abspath = os.path.dirname(__file__)
#sys.path.append(abspath)
#os.chdir(abspath)
import web
import config
import app.controllers

from app.helpers import custom_error

urls = (
	# index 
	'/',											'app.controllers.base.Index',

	'/sample',										'app.controllers.base.Sample',

	'/about',										'app.controllers.base.About',

	'/directory',									'app.controllers.base.Directory',
	'/file',										'app.controllers.base.File',
	'/save',										'app.controllers.base.Save',

	# signin, signup, signout
	'/signin',										'app.controllers.account.Signin',
	'/signout',										'app.controllers.account.Signout',
	'/signup',										'app.controllers.account.Signup',

	# return given file, need for ajax file load
	'/return',										'app.controllers.base.Return',

	# compile, run
	'/compile',										'app.controllers.compiler.Compile',
	'/run',											'app.controllers.compiler.Run',

	# let server handle in production
	'/(?:css|images|scripts|fonts).+',				'app.controllers.public.Public',
	'/favicon.ico',									'app.controllers.public.Public',
)

	
app = web.application(urls, globals())
custom_error.add(app)

application = app.wsgifunc()

if __name__ == '__main__':
	app.run()