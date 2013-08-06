#!/usr/bin/python
#encoding: utf-8

import os
import core
from datetime import datetime
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

TEMPLATE_FILE='index.tpl'


env = Environment()
env.loader = FileSystemLoader('.')
template = env.get_template(TEMPLATE_FILE)

items=[]
for i in xrange(len(core.descFiles)):
	try:
		lastUpdate = datetime.fromtimestamp(os.path.getmtime(os.path.join(core.dataDir, "dados_%s.jsonlines" % core.validFiles[i])))
	except OSError:
		lastUpdate = None

	formats=[]
	for format in core.validFormats:
		try:
			fileSize = os.path.getsize(os.path.join(core.dataDir, "dados_%s.%s" % (core.validFiles[i], format))) / 1024.0 / 1024.0
		except:
			fileSize = None

		formats.append({format : fileSize})

	items.append({'desc': core.descFiles[i], 'filename': core.validFiles[i], 'formats': formats, 'lastUpdate': lastUpdate})


print "Content-Type: text/html\r\n"
print template.render(items=items).encode('utf-8')

