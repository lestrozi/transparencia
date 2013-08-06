#!/usr/bin/python

import os
import sys
import cgi
import cgitb
import core

cgitb.enable()

get = cgi.FieldStorage()
try:
	filename = get.getlist('filename')[0]
	format = get.getlist('format')[0]

	assert filename in core.validFiles
	assert format in core.validFormats
except:
	print "Usage:"
	print "/dados.py?filename={%s}&format={%s}" % ('|'.join(core.validFiles), '|'.join(core.validFormats))
	quit()



print "Content-Type: application/octet-stream"
print "Content-Disposition: attachment;filename=\"%s.%s\"\r\n" % (filename, format)

file = os.path.join(core.dataDir, 'dados_%s.%s' % (filename, format))

f = open(file)
sys.stdout.write(f.read())
f.close()

