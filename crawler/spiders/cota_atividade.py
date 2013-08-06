import json
import re
import urllib
from datetime import datetime
from decimal import Decimal
from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from crawler.items import CotaParlamentarItem, my_norm, similar


class CotaParlamentar(BaseSpider):
	name = "cotaParlamentar"

	minDate = datetime.min
	start_urls = ['http://www.camara.gov.br/cota-parlamentar/']

        def __init__(self, minDate=None):
		if minDate != None:
			(mes, ano) = minDate.split('/')
			self.minDate = datetime(int(ano), int(mes), 1)


	def parse(self, response):
		hxs = HtmlXPathSelector(response)

		lista = hxs.select('//select[@id="listaDep"]/option')

		for deputado in lista:
			id = ''.join(deputado.select('@value').extract()).strip()
			nome = ''.join(deputado.select('text()').extract()).strip()

			if id == 'QQ':
				continue

			today = datetime.today()
			mes = today.month-1
			ano = today.year

			yield Request("http://www.camara.gov.br/cota-parlamentar/cota-sumarizado?nuDeputadoId=%s&mesAnoConsulta=%s%%2F%s" % (id, mes, ano), callback=self.parsedatas, meta={'deputado': nome, 'id': id})


	def parsedatas(self, response):
		hxs = HtmlXPathSelector(response)

		listaDatas = hxs.select('//*[@id="mesAno"]/option/@value').extract()

		id = response.meta['id']

		for data in listaDatas:
			(mes, ano) = re.split('[-\/]', data)

			if datetime(int(ano), int(mes), 1) >= self.minDate:
				yield Request("http://www2.camara.leg.br/transparencia/cota-para-exercicio-da-atividade-parlamentar/verba_indenizatoria_detalheVerbaAnalitico?nuDeputadoId=%s&numMes=%s&numAno=%s&numSubCota=" % (id, mes, ano), callback=self.parsedados, meta={'deputado': response.meta['deputado'], 'mes': mes, 'ano': ano})
			


	def parsedados(self, response):
		hxs = HtmlXPathSelector(response)

		divs = hxs.select('//*[@id="content"]/div/div/div')
		for div in divs:
			for entrada in div.select('table/tbody/tr'):
				item = CotaParlamentarItem()

				item['deputado'] = response.meta['deputado']
				item['mes'] = response.meta['mes']
				item['ano'] = response.meta['ano']
				item['titulo']=my_norm(''.join(div.select('h4/text()').extract()).strip())
				item['cpfcnpj']=''.join(entrada.select('td[1]/text()').extract()).strip()
				item['nome']=my_norm(''.join(entrada.select('td[2]/text()').extract()).strip())
				item['nfrecibo']=''.join(entrada.select('td[3]/text()').extract()).strip()
				valor=''.join(entrada.select('td[last()]/text()').extract()).strip()

				try:
					valor = valor.replace('.', '')
					valor = valor.replace(',', '.')
					valor = valor.split('$')[1].strip()
					valor = Decimal(valor)
				except:
					valor = Decimal('-1.00')

				item['valor'] = valor

				yield item

