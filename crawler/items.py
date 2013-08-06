import re
import difflib
import unicodedata
from scrapy.item import Item, Field


def my_norm(str):
	return unicodedata.normalize('NFD', str.strip().upper()).encode('ascii', 'ignore')


def similar(str1, str2):
	return difflib.SequenceMatcher(None, str1, str2).ratio() > 0.8


def extract_tels(tels):
    listatels = []
    
    for v in re.findall('(\(?\d?(\d\d)\)?\s?)?(\d\d\d\d?\d?)[^\d]?(\d\d\d\d)', tels, re.DOTALL):
        listatels.append('(%s) %s-%s' % (v[1], v[2], v[3]) if v[1] else '%s-%s' % (v[2], v[3]))
        
    return listatels


class TransparenciaItem(Item):
	deputado = Field()
	favorecido = Field()


class DeputadoItem(Item):	
	nome_urna = Field()
	nome_completo = Field()
	partido = Field()
	uf = Field()
	telefone = Field()

	def __str__(self):
		return '[nome_urna=%s, nome_completo=%s, partido=%s, UF=%s, telefone=%s]' % (self['nome_urna'], self['nome_completo'], self['partido'], self['uf'], self['telefone'],)

class PrestacaoContasItem(Item):
	deputado = Field()
	doador = Field()
	cpfcnpj = Field()
	valor = Field()

class CotaParlamentarItem(Item):
	deputado = Field()
	mes = Field()
	ano = Field()
	titulo = Field()
	cpfcnpj = Field()
	nome = Field()
	nfrecibo = Field()
	valor = Field()
