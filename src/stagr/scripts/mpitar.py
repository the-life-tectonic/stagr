#!/usr/bin/env python
import atexit
import argparse
import tarfile
import threading
from mpi4py import MPI

class MPIIterator(threading.Thread):
    NEXT=4242
    STOP_ITERATION=4243

    def __init__(self,items,source_rank=0,comm=MPI.COMM_WORLD):
        self.source_rank=0
        self.mpi_comm=comm
        self.mpi_rank=comm.Get_rank()
        self.mpi_size=comm.Get_size()
        super(MPIIterator, self).__init__()
        if self.mpi_rank==self.source_rank:
            self._iter=iter(items);
            self.start()

    def __iter__(self):
        return self

    def next(self):
        if self.mpi_rank==self.source_rank:
            return self._iter.next()
        else:
            self.mpi_comm.send(None,dest=self.source_rank,tag=MPIIterator.NEXT)
            status=MPI.Status()
            self.mpi_comm.Probe(source=self.source_rank, tag=MPI.ANY_TAG, status=status)
            if status.tag==MPIIterator.STOP_ITERATION:
                raise self.mpi_comm.recv(source=self.source_rank, tag=MPIIterator.STOP_ITERATION)
            elif status.tag==MPIIterator.NEXT:
                return self.mpi_comm.recv(source=self.source_rank, tag=MPIIterator.NEXT)

    def run(self):
        mpi_stopped=0
        while True:
            status=MPI.Status()
            self.mpi_comm.Probe(source=MPI.ANY_SOURCE, tag=MPIIterator.NEXT, status=status)
            self.mpi_comm.recv(source=status.source, tag=MPIIterator.NEXT)
            try:
                item=self._iter.next()
                self.mpi_comm.send(item,dest=status.source,tag=MPIIterator.NEXT)
            except StopIteration as item:
                self.mpi_comm.send(item,dest=status.source,tag=MPIIterator.STOP_ITERATION)
                mpi_stopped+=1
                if mpi_stopped==self.mpi_comm.Get_size()-1:
                    break;

class  MPILog(threading.Thread):
    TAG_DONE=4580
    TAG_LOG=4581

    def __init__(self,comm=MPI.COMM_WORLD,logger_rank=0):
        self.logger_rank=logger_rank
        self.mpi_comm=comm
        self.mpi_rank=comm.Get_rank()
        self.mpi_size=comm.Get_size()
        super(MPILog, self).__init__()
        if self.mpi_rank==self.logger_rank:
            atexit.register(self.join)
            self.start()
        else:
            atexit.register(self.send_done)

    def log(self,msg):
        self.mpi_comm.send(msg,dest=self.logger_rank,tag=MPILog.TAG_LOG)

    def send_done(self):
        self.mpi_comm.send(dest=self.logger_rank,tag=MPILog.TAG_DONE)

    def run(self):
        mpi_stopped=0
        while True:
            status=MPI.Status()
            self.mpi_comm.Probe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG,status=status)
            if status.tag==MPILog.TAG_LOG:
                data = self.mpi_comm.recv(source=status.source, tag=MPILog.TAG_LOG)
                print("[%03d] %s"%(status.source,data))
            elif status.tag==MPILog.TAG_DONE:
                self.mpi_comm.recv(source=status.source, tag=MPILog.TAG_DONE)
                mpi_stopped+=1
                if mpi_stopped==self.mpi_comm.Get_size()-1:
                    break;

class TarFilterLogger(object):
    def __init__(self,log):
        self.log=log

    def __call__(self,tarinfo):
        self.log.log(tarinfo.name)
        return tarinfo

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Creats a TAR archive for each file listed using MPI to parallelize the process')
    parser.add_argument('files',help='The files or directory to archive',nargs="+")
    parser.add_argument('-j',dest='bz2',action='store_true',help='Use bz2 compression',default=False)
    parser.add_argument('-z',dest='gzip',action='store_true',help='Use gzip compression',default=False)
    parser.add_argument('-v',dest='verbose',action='store_true',help='Verbose output',default=False)
    args=parser.parse_args()

    log=MPILog()

    filter=None
    if args.verbose:
        filter=TarFilterLogger(log)
        
    for filename in MPIIterator(args.files):
        mode="w"
        filename_out=filename+".tar"
        if args.bz2:
            filename_out=filename_out+'.bz2'
            mode="w:bz2"
        elif args.gzip:
            filename_out=filename_out+'.gz'
            mode="w:gz"
        if args.verbose:
            log.log("creating %s" % filename_out)
        tar=tarfile.open(filename_out,mode)
        tar.add(filename,filter=filter)
        tar.close()
    if args.verbose:
        log.log("done")
