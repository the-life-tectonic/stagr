import os
import stat
from datetime import datetime
from setuptools import setup

def read(fname):
	    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def most_recent_mod(directory):
	mod=0;
	for dirpath, dirnames, filenames in os.walk(directory): 
		for filename in filenames:
			fname=os.path.join(dirpath,filename)
			stats=os.stat(fname)
			mod=max(mod,stats[stat.ST_MTIME])
	return mod

src='src/stagr'

ver=datetime.fromtimestamp(most_recent_mod(src)).strftime('%Y.%m.%d.%H.%M')

setup(
	name='stagr_mod',
	description='Python based report generator for StagYY',
	author='Robert I. Petersen',
	author_email='rpetersen@ucsd.edu', 
	version=ver,
	scripts=['src/stagr/scripts/pardiff.py','src/stagr/scripts/stagr.py','src/stagr/scripts/stagr','src/stagr/scripts/mpitar.py'],
	packages=['stagr_mod'],
	package_dir={'stagr_mod': 'src/stagr'},
	package_data={'stagr_mod':['templates/*.html','templates/*.pyt','templates/style/*','templates/js/*','templates/err/*']},
	license='GPL 2.0', 
	classifiers=[
'Development Status :: 4 - Beta',
'Intended Audience :: Developers',
'License :: OSI Approved :: GNU General Public License (GPL)',
'Programming Language :: Python'
	],
	long_description=read('README')
)
