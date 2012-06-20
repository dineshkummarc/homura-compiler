import random
import os, subprocess
import types
import StringIO
import string


def get_all_functions(module):
	functions = {}
	for f in [module.__dict__.get(a) for a in dir(module)
		if isinstance(module.__dict__.get(a), types.FunctionType)]:
		functions[f.__name__] = f
	return functions



def genstr(length = 6):
	return ''.join([random.choice(string.ascii_lowercase) for i in xrange(length)])


def whereis(program):
	for path in os.environ.get('PATH', '').split(':'):
		if os.path.exists(os.path.join(path, program)) and \
			not os.path.isdir(os.path.join(path, program)):
			return os.path.join(path, program)
	return None


def compile_cpp(workdir, run, source):
	# makedir + ch dir
	if not os.path.exists(workdir + run):
		os.mkdir(workdir + run)
		
	os.chdir(workdir + run)

	inputfile = 'a.cpp'
	outputfile = 'a'

	for f in [inputfile, outputfile]:
		if os.path.exists(f): os.remove(f)

	# create file
	f = open(inputfile, 'w')
	f.write(source+'\n')
	f.close()

	process = subprocess.Popen(['g++', inputfile, '-o', outputfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

	output, error = process.communicate()

	process.wait()

	os.chdir('../..')
	
	# if compiled successfully, return None
	if process.returncode == 0: return None

	# return error message
	return error
#end compile_cpp


def compile_java(workdir, run, source):
	# makedir + ch dir
	if not os.path.exists(workdir + run):
		os.mkdir(workdir + run)
		
	os.chdir(workdir + run)

	inputfile = 'Solution.java'

	for f in os.listdir('.'):
		if os.path.exists(f): os.remove(f)

	# create file
	f = open(inputfile, 'w')
	f.write(source+'\n')
	f.close()

	process = subprocess.Popen(['javac', inputfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

	output, error = process.communicate()

	process.wait()

	os.chdir('../..')
	
	# if compiled successfully, return None
	if process.returncode == 0: return None

	# return error message
	return error
#end compile_cpp


def compile_csharp(workdir, run, source):
	# makedir + ch dir
	if not os.path.exists(workdir + run):
		os.mkdir(workdir + run)

	os.chdir(workdir + run)

	inputfile = 'a.cs'
	outputfile = 'a.exe'

	for f in os.listdir('.'):
		if os.path.exists(f): os.remove(f)

	# create file
	f = open(inputfile, 'w')
	f.write(source+'\n')
	f.close()

	process = subprocess.Popen(['gmcs', inputfile, '-out:%s'%outputfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

	output, error = process.communicate()

	process.wait()

	os.chdir('../..')

	# if compiled successfully, return None
	if process.returncode == 0: return None

	# return error message
	return error
#end compile_cpp



def run_cpp(workdir, run, theinput):
	# makedir + ch dir
	if not os.path.exists(workdir + run):
		return 'Exe dir not found. \n please compile it again'

	os.chdir(workdir + run)

	exefile = './a'

	if not os.path.exists(exefile):
		return 'Exe file not found. \n please compile it again'

	process = subprocess.Popen(exefile, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

	output, error = process.communicate(theinput)

	process.wait()

	os.chdir('../..')

	return (process.returncode, output)
#end compile_cpp


def run_java(workdir, run, theinput):
	# makedir + ch dir
	if not os.path.exists(workdir + run):
		return 'Exe dir not found. \n please compile it again'

	os.chdir(workdir + run)

	exefile = 'Solution.class'

	if not os.path.exists(exefile):
		return 'Exe file not found. \n please compile it again'

	process = subprocess.Popen(['java', exefile.split('.')[0]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

	output, error = process.communicate(theinput)

	process.wait()

	os.chdir('../..')

	return (process.returncode, output)
#end compile_cpp


def run_csharp(workdir, run, theinput):
	# makedir + ch dir
	if not os.path.exists(workdir + run):
		return 'Exe dir not found. \n please compile it again'

	os.chdir(workdir + run)

	exefile = 'a.exe'

	if not os.path.exists(exefile):
		return 'Exe file not found. \n please compile it again'

	process = subprocess.Popen(['mono', exefile], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

	output, error = process.communicate(theinput)

	process.wait()

	os.chdir('../..')

	return (process.returncode, output)
#end compile_cpp

