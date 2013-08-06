import re
import json
import urllib
from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest
from crawler.items import PrestacaoContasItem, my_norm, similar


class PrestacaoContas(BaseSpider):
	name = "prestacaoContas"

	start_urls = ['http://spce2010.tse.jus.br/spceweb.consulta.prestacaoconta2010/pesquisaCandidato.jsp']

	def __init__(self):
		pass


	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		
		UFs = hxs.select('//*[@id="sgUe"]/option/@value').extract()
		for UF in UFs:
			if UF != '':
				yield FormRequest.from_response(response, formnumber=0, formdata={'acao':'pesquisar','sgUe':UF,'candidatura':'6','parcial':'0'}, callback=self.parseform, meta={'uf':UF})


	def parseform(self, response):
		hxs = HtmlXPathSelector(response)
		pessoas = hxs.select('//td[2]/a[contains(@onclick,"setSq")]')

		if len(pessoas) < 1:
			log.msg("Ninguem encontrado para [%s]" % response.url, level=log.ERROR)
			return

		nomesIds = {}
		for pessoa in pessoas:
			matches = re.search("^setSqCandidato\('(\d+)'", pessoa.select('@onclick').extract()[0])
			if not matches:
				log.msg("setSqCandidato regexp nao encontrada: [%s]" % response.url, level=log.ERROR)
				return

			nome = my_norm(''.join(pessoa.select('text()').extract()).strip())
			id = matches.group(1)

			nomesIds[nome]=id

			yield Request('http://spce2010.tse.jus.br/spceweb.consulta.receitasdespesas2010/resumoReceitasByCandidato.action?filtro=N&sqCandidato=%s&sgUe=%s&nomeVice=null' % (id, response.meta['uf']), callback=self.parsedados, meta={'deputado': nome})
			


	def parsedados(self, response):
		hxs = HtmlXPathSelector(response)

		for entrada in hxs.select('//table/tr/td/table[2]/tr'):
			doador = my_norm(''.join(entrada.select('td[1]/text()').extract()).strip())

			if my_norm(unicode(doador)) == 'DOADOR':
				continue

			item = PrestacaoContasItem()
			item['deputado'] = response.meta['deputado']
			item['doador'] = doador
			item['cpfcnpj'] = ''.join(entrada.select('td[2]/text()').extract()).strip()
			item['valor'] = ''.join(entrada.select('td[5]/text()').extract()).strip()
			item['valor'] = float(item['valor'].replace(',', ''))

			yield item

