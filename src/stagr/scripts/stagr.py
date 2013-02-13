import argparse
import logging
import fnmatch
import os
import shutil
import sys
import tempfile

import matplotlib 
matplotlib.use('agg') 

from webob import Request
from webob import Response
import of_util.path
import stagyy.io as sio
import stagyy.viz as viz
import stagyy.field as stagyy_field
import of_pyt.template as pyt
import stagr_mod
#from settings import template_dir, working_dir
template_dir=stagr_mod.templateDir
working_dir=os.path.expanduser("~/tmp/stagr/")
if not os.path.exists(working_dir):
	os.makedirs(working_dir)

# Get the template directory
# Get the working directory


# By default we arn't verbose
verbose=False
# Setup a logger and formatter
name = os.path.basename(sys.argv[0])
logger = logging.getLogger(name)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s")

plotable_fields=['t','eta','ed','rho']

def write_null(body_data):
	pass

def start_response(status, response_headers, exc_info=None):
	return write_null

def process_template(template,html_out,suite,docstore):
	template_file=os.path.join(template_dir,template[1:])
	logger.debug('Rendering template "%s" from %s to "%s"'%(template,template_file,html_out))
	req = Request.blank(template)
	req.suite=suite
	req.fields=plotable_fields
	resp = Response( charset='utf8' )
	content=docstore.get_content( template_file )
	content(req,resp)
	iterator=resp(req.environ,start_response)
	out=open(html_out,'w')
	for i in iterator:
		out.write(i)
	out.close()

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
	logger.info("Program completed")

def build_report(suite,report_dir,docstore):
	# Copy static files
	logger.debug('Copying static file from %s to %s',template_dir,report_dir)
	of_util.path.copyr(template_dir,report_dir,ignore=shutil.ignore_patterns('*.pyt'))
	# build the template pages
	extensions={ '/js/*':'.js', '/css/*':'css' }
	for template in docstore.get_docs(template_dir,'*.pyt'):
		logger.debug('processing template %s'%template)
		filename,ext=os.path.splitext(template)
		ext='.html'
		for pattern in extensions.keys():
			if fnmatch.fnmatch(template,pattern ) :
				ext=extensions[pattern]
				break
		process_template(template,os.path.join(report_dir,filename[1:]+ext),suite,docstore)

	for model in suite.models:
		# build the report directory structure
		logger.debug('Writing report for model %s',model.name)
		model_dir=os.path.join(report_dir,model.name)
		if not os.path.exists(model_dir): os.makedirs(model_dir)
		h5_dir=os.path.join(model_dir,'data')
		if not os.path.exists(h5_dir): os.makedirs(h5_dir)
		plot_dir=os.path.join(model_dir,'plots')
		if not os.path.exists(plot_dir): os.makedirs(plot_dir)

		# Make/update the H5 files
		model_fields=[stagyy_field.by_prefix[prefix] for prefix in sorted(set(plotable_fields)&set(model.fields))]
		try:
			h5_files=sio.model_to_h5(model,h5_dir,model_fields)
			# Plot the fileds
			for h5_file in h5_files:
				viz.plot_2D(h5_file['filename'],plot_dir)
		except:
			logger.error('Exception creating h5 files for model %s at %s',model.name,model.dir,exc_info=True)
		# Plot the timesteps
		viz.plot_modeltime(model.timesteps,model.plot_file_prefix,plot_dir,title='%s model years per timestep'%model.name,ts_max=suite.max_last_timestep)


if __name__ == "__main__":
	import atexit
	atexit.register(logExit)
	# Set up the screen handler for errors
	screen_handler=logging.StreamHandler()
	screen_handler.setFormatter(formatter)
	screen_handler.setLevel(logging.ERROR)
	logger.addHandler(screen_handler)

	parser = argparse.ArgumentParser('Description of program goes here')
#	parser.add_argument('--id',required=False,help='The job id',default=None)
	parser.add_argument('-s',dest='suite',required=True,help='Model suite directory')
	parser.add_argument('-r',dest='report',required=True,help='Report directory')
	parser.add_argument('-v',dest='verbose',action='store_true',help='Verbose output')
	parser.add_argument('-q',dest='quiet',action='store_true',help='Suppresses non-error screen output')
	parser.add_argument('-l',dest='log',help='log file',default=None)
	args=parser.parse_args()

	if args.log!=None:
		enable_file_log(args.log)

	if args.verbose:
		screen_handler.setLevel(logging.DEBUG)
		sio.LOG.setLevel(logging.DEBUG)
		viz.LOG.setLevel(logging.DEBUG)
		logger.setLevel(logging.DEBUG)
		map(sio.LOG.addHandler,logger.handlers)
		map(viz.LOG.addHandler,logger.handlers)
	
	if args.quiet:
		screen_handler.setLevel(logging.ERROR)

	# Setup the suite, report and docstore
	suite=sio.Suite(args.suite)
	report_dir=os.path.join(args.report,suite.name)
	docstore=pyt.DocumentStore(working_dir,check_mod=True)
	build_report(suite,report_dir,docstore)






