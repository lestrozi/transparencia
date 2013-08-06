import sys
import argparse
import json
import dicttoxml

supportedFormats = ['json', 'xml']


class XMLCreator:
	f = None

	def __init__(self, f):
		self.f = f
		self.f.write('<?xml version="1.0" encoding="UTF-8" ?><root>')

	def append(self, dict):
		#str = dicttoxml.dicttoxml(dict)
		#str = str[45:-7]
		str = ''.join(["<%s>%s</%s>" % (k, v, k) for k,v in dict.items()])	#not great, but very fast
		self.f.write('<item>' + str.encode('utf8') + '</item>')

	def finish(self):
		self.f.write('</root>')
		

class JSONCreator:
	f = None
	first = True

	def __init__(self, f):
		self.f = f
		self.f.write('[')

	def append(self, dict):
		str = json.dumps(dict)
		if not self.first:
			self.f.write(', ')

		self.f.write(str.encode('utf8'))
		self.first = False

	def finish(self):
		self.f.write(']')
		


parser = argparse.ArgumentParser(description='Convert JSON-lines to other formats')
parser.add_argument('--input', '-i', dest='filename', required=True, help='input file')
parser.add_argument('--to', '-t', choices=supportedFormats, required=True, help='output format')

args = parser.parse_args()


foutput = sys.stdout
if args.to == 'xml':
	creator = XMLCreator(foutput)
elif args.to == 'json':
	creator = JSONCreator(foutput)


with open(args.filename) as f:
	for line in f:
		jsonLine = line.rstrip()
		dict = json.loads(jsonLine)

		creator.append(dict)

creator.finish()

