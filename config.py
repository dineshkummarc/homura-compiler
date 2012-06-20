import web
import cgi

from app.helpers import utils, formatting


db = web.database(dbn='mysql', db='compiler', user='miku', passwd='miku', charset=None)

cache = False

web.config.debug = True

# template global functions
globals_ = utils.get_all_functions(formatting)

# set global base template
view = web.template.render('app/views', cache=cache, globals=globals_)

# Maximum input we will accept when REQUEST_METHOD is POST
# 0 ==> unlimited input
cgi.maxlen = 10 * 1024 * 1024 # 10MB
