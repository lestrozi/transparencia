from scrapy.conf import settings


class DefPipeline(object):
	favorecidos = {}
	
	def __init__(self):
		pass


	def process_item(self, item, spider):
		return item


	def close_spider(self, spider):
		pass
