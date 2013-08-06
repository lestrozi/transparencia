import re
from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from crawler.items import DeputadoItem, my_norm, extract_tels


class DadosDeputados(BaseSpider):
	name = "dadosDeputados"
	start_urls = [
		"http://www2.camara.leg.br/deputados/pesquisa",
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		dados = ['xxx'.join(item.select('@value').extract()) for item in hxs.select('//*[@id="deputado"]/option')]

		for dado in dados:
			if dado == '':
				continue
		
			tmp = dado.split('?')
			if len(tmp) != 2:
				log.msg("ERRO! Esperado: XXXXXX?999, Recebido: %s" % dado, level=log.ERROR)
				continue
				
			id = tmp[1]
		
			url = 'http://www.camara.leg.br/internet/Deputado/dep_Detalhe.asp?id=%s' % id

			request = Request(url, callback=self.parse_dados)
			yield request


	def parse_dados(self, response):
		hxs = HtmlXPathSelector(response)

		dados = [v.strip() for v in hxs.select('//*[@id="content"]/div/div/ul/li/text()').extract()]
		
		deputado = DeputadoItem()
		deputado['nome_urna'] = my_norm(re.sub('^Deputado ', '', ''.join(hxs.select('//*[@id="portal-mainsection"]/h2/text()').extract()).strip()))
		deputado['nome_completo'] = my_norm(dados[0])
		deputado['partido'], deputado['uf'] = [my_norm(v) for v in dados[3].split(' / ')[:2]]
		deputado['telefone'] = ' / '.join(extract_tels(my_norm(dados[4])))
		
		yield deputado
