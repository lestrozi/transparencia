#!/usr/bin/python

import os
import shlex
import threading
import subprocess
from crawler.settings import BASEDIR


CONVERT=os.path.join(BASEDIR, 'convert.py')
DATADIR=os.path.join(BASEDIR, 'resultado/')

formats = ['xml', 'json', 'jsonlines']
spiders = []

p=subprocess.Popen(['scrapy', 'list'], cwd=BASEDIR, stdout=subprocess.PIPE)
for line in p.stdout:
	spiders.append(line.rstrip())



def popenAndCall(onExit, meta, popenArgs, workDir):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    onExit when the subprocess completes.
    onExit is a callable object, and popenArgs is a list/tuple of args that 
    would give to subprocess.Popen.
    """
    def runInThread(onExit, meta, popenArgs, workDir):
        proc = subprocess.Popen(popenArgs, cwd=workDir)
        proc.wait()
        onExit(meta)
        return

    thread = threading.Thread(target=runInThread, args=(onExit, meta, popenArgs, workDir))
    thread.start()

    # returns immediately after the thread starts
    return thread


def onExit(meta):
	src = '%sdados_%s.jsonlines.incomplete' % (DATADIR, meta)
	dst = '%sdados_%s.jsonlines' % (DATADIR, meta)
	os.rename(src, dst)

        for format in formats:
		if format != 'jsonlines':	#it's already in jsonlines
			src = '%sdados_%s.%s.incomplete' % (DATADIR, meta, format)
			dst = '%sdados_%s.%s' % (DATADIR, meta, format)

			outfile = open(src, 'w')
			p = subprocess.Popen(shlex.split('python2.7 %s -i %sdados_%s.jsonlines -t %s' % (CONVERT, DATADIR, meta, format)), stdout=outfile)
			p.wait()
			outfile.flush()
			outfile.close()

			os.rename(src, dst)
                

		src = '%sdados_%s.%s.incomplete.gz' % (DATADIR, meta, format)
		dst = '%sdados_%s.%s.gz' % (DATADIR, meta, format)

		outfile = open(src, 'wb')
		p = subprocess.Popen(shlex.split('gzip -c %sdados_%s.%s' % (DATADIR, meta, format)), stdout=outfile)
		p.wait()
		outfile.flush()
		outfile.close()

		os.rename(src, dst)


for dado in spiders:
	popenAndCall(onExit, dado, shlex.split('scrapy crawl %s' % dado), BASEDIR)

