import web
from config import view
from web import form
import json, re
import os, shutil, subprocess

from app.helpers import render
from app.helpers import utils

class Compile:
	def GET(self):
		return 'hello world'

	def POST(self):
		source = web.input(source='')['source']
		language = web.input(language='')['language']
		run = web.input(run='')['run']

		# if incorrect run id, regenerate it
		if re.match('^[a-z]{5,12}$', run) == None: run = utils.genstr(12)

		workdir = 'work/'

		# first state of result
		result = 'unknown language'

		if language == 'cpp':
			result = utils.compile_cpp(workdir, run, source)
		elif language == 'java':
			result = utils.compile_java(workdir, run, source)
		elif language == 'csharp':
			result = utils.compile_csharp(workdir, run, source)

		if result == None:
			return json.dumps(
				{'status': 'OK', 'message': 'Successfully compiled.', 'run': run })

		return json.dumps(
			{'status': 'CE', 'message': result, 'run': run })

# end Compile


class Run:
	def POST(self):
		language = web.input(language='')['language']
		run = web.input(run='')['run']
		theinput = web.input(input='')['input']

		# if incorrect run id, exit
		if re.match('^[a-z]{5,12}$', run) == None: return 'incorrect run id'

		workdir = 'work/'

		# first state of result
		output = 'unknown language'

		if language == 'cpp':
			output = utils.run_cpp(workdir, run, theinput)
		elif language == 'java':
			output = utils.run_java(workdir, run, theinput)
		elif language == 'csharp':
			output = utils.run_csharp(workdir, run, theinput)

		if output[0] == 0:
			return json.dumps(
				{'status': 'OK', 'output': output[1] })

		return json.dumps(
			{'status': 'RE', 'output': ('Runtime error %s \n %s' % (output[0], output[1])) })
# end Run
