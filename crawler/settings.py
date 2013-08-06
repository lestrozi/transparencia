import os

ITEM_PIPELINES = [
    'crawler.pipelines.DefPipeline'
]

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
USER_AGENT = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

FEED_FORMAT = 'jsonlines'
FEED_URI = 'file://%s/dados_%%(name)s.jsonlines.incomplete' % os.path.join(BASEDIR, 'resultado')

LOG_LEVEL = 'INFO'
LOG_FILE = '%s/scrapy.log' % BASEDIR

CONCURRENT_ITEMS = 32
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 3
DOWNLOAD_DELAY = 0.5
RANDOMIZE_DOWNLOAD_DELAY = True

RETRY_TIMES = 3
