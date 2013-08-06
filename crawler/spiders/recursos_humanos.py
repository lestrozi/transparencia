from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from crawler.items import TransparenciaItem, my_norm


class RecursosHumanos(BaseSpider):
	name = "recursosHumanos"
	start_urls = [
		"http://www2.camara.leg.br/transparencia/recursos-humanos/quadro-remuneratorio/consulta-secretarios-parlamentares",
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		dados = [('xxx'.join(item.select('@value').extract()),'xxx'.join(item.select('text()').extract())) for item in hxs.select('//*[@id="lotacao"]/option')]

		for dado in dados:
			if dado[0] == '':
				continue

			url = 'http://www2.camara.leg.br/transparencia/recursos-humanos/quadro-remuneratorio/consulta-secretarios-parlamentares/layouts_transpar_quadroremuner_consultaSecretariosParlamentares?form.button.pesquisar=Pesquisar&b_start:int=0&lotacao=%s' % dado[0]

			request = Request(url, callback=self.parse_dados)
			request.meta['deputado'] = dado[1]
			yield request


	def parse_dados(self, response):
		hxs = HtmlXPathSelector(response)
		
		favs = [''.join(item.select('td[2]/text()').extract()) for item in hxs.select('//*[@id="content"]/div/div/table/tbody/tr')]

		deputado = response.meta['deputado']

		for fav in favs:
			item = TransparenciaItem()
			item['deputado'] = my_norm(deputado)
			item['favorecido'] = my_norm(fav)
			yield item

		nextUrl = hxs.select('//*[@id="content"]/div/div/div/span[@class="next"]/a/@href').extract()

		if nextUrl:
			request = Request(''.join(nextUrl), callback=self.parse_dados)
			request.meta['deputado'] = deputado
			yield request
