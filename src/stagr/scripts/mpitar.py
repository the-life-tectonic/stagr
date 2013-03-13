#!/usr/bin/env python
import sys
import argparse
import tarfile
from mpi4py import MPI

def log(s):
	print("%02d/%02d - %s"%(rank,size,s))

if __name__ == "__main__":
	parser = argparse.ArgumentParser('Creats a TAR archive for each file listed using MPI to parallelize the process')
	parser.add_argument('files',help='The files or directory to archive',nargs="+")
	parser.add_argument('-j',dest='bz2',action='store_true',help='Use bz2 compression',default=False)
	parser.add_argument('-z',dest='gzip',action='store_true',help='Use gzip compression',default=False)
	parser.add_argument('-v',dest='verbose',action='store_true',help='Verbose output',default=False)
	args=parser.parse_args()

	comm=MPI.COMM_WORLD
	rank=comm.Get_rank()
	size=comm.Get_size()
	ndx_files=range(rank,len(args.files),size)
	log("Will process %s"%ndx_files)
	for n in ndx_files:
		mode="w"
		filename=args.files[n]
		filename_out=filename+".tar"
		if args.bz2:
			filename_out=filename_out+'.bz2'
			mode="w:bz2"
		elif args.gzip:
			filename_out=filename_out+'.gz'
			mode="w:gz"
		tar=tarfile.open(filename_out,mode)
		tar.add(filename)
		tar.close()
