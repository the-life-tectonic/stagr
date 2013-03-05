import argparse
import logging
import fnmatch
import os
import shutil
import sys
import tempfile

from glob import glob

import stagyy.io as sio

# By default we arn't verbose
verbose=False
# Setup a logger and formatter
name = os.path.basename(sys.argv[0])
logger = logging.getLogger(name)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s")

def enable_file_log(name):
	file_handler=logging.FileHandler(name)
	file_handler.setFormatter(formatter)
	if verbose:
		file_handler.setLevel(logging.DEBUG)
	else:
		file_handler.setLevel(logging.INFO)
	logger.addHandler(file_handler)
	return file_handler

def logExit():
	logger.debug("Program completed")

if __name__ == "__main__":
	import atexit
	atexit.register(logExit)
	# Set up the screen handler for errors
	screen_handler=logging.StreamHandler()
	screen_handler.setFormatter(formatter)
	screen_handler.setLevel(logging.ERROR)
	logger.addHandler(screen_handler)

	parser = argparse.ArgumentParser('Description of program goes here')
	parser.add_argument('-m',dest='model',required=True,help='Model directory')
	parser.add_argument('-f',dest='field',required=True,help='Data field output to use, default "vp"',default="vp")
	parser.add_argument('-v',dest='verbose',action='store_true',help='Verbose output')
	parser.add_argument('-q',dest='quiet',action='store_true',help='Suppresses non-error screen output')
	parser.add_argument('-l',dest='log',help='log file',default=None)
	args=parser.parse_args()

	if args.log!=None:
		enable_file_log(args.log)

	if args.verbose:
		screen_handler.setLevel(logging.DEBUG)
		sio.LOG.setLevel(logging.DEBUG)
		logger.setLevel(logging.DEBUG)

	map(sio.LOG.addHandler,logger.handlers)
	
	if args.quiet:
		screen_handler.setLevel(logging.ERROR)

	# Setup the suite, report and docstore
	par = sio.Par(args.model)

	tpf=int(p['timein']['nwrite'])
	logger.debug('%d timesteps per frame',pattern)

	pattern=os.path.join(args.model,par['ioin']['output_file_stem']+'_'+args.field+'*')
	logger.debug('Using files %s',pattern)

	ctime=np.array([ os.stat(f).st_ctime  for f in glob(pattern)]
	logger.debug('Found %d frames',len(ctime)

	delta=ctime[:-1]-ctime[1:]
	# Calculate timesteps per minute
	tpm=60*tpf/delta
	print("Average: %0.1f"%np.average(tpm))
	print("Min: %0.1f"%np.min(tpm))
	print("Max: %0.1f"%np.max(tpm))


