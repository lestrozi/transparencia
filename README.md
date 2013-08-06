Transpar�ncia
=============
- Cota Parlamentar - spiders/cota_atividade.py - Crawler de http://www.camara.gov.br/cota-parlamentar/ (suporta data de in�cio, mas ainda n�o est� sendo usado)
- Dados de deputados - spiders/dados_deputados.py - Crawler de http://www2.camara.leg.br/deputados/pesquisa
- Presta��o de contas de campanha - spiders/prestacao_contas.py - Crawler de http://spce2010.tse.jus.br/spceweb.consulta.prestacaoconta2010/pesquisaCandidato.jsp
- Recursos humanos - spiders/recursos_humanos.py - http://www2.camara.leg.br/transparencia/recursos-humanos/quadro-remuneratorio/consulta-secretarios-parlamentares

Instala��o sugerida:
====================
1. Coloque os arquivos do diret�rio www/ em um diret�rio acess�vel por HTTP (como exemplo, ser� usado /var/www/html)
2. Crie o diret�rio /var/www/dados (n�o acess�vel pelo httpd, mas com permiss�o para o usu�rio do httpd acessar): chown apache: /var/www/dados
3. Instale os outros arquivos no diret�rio desejado (como exemplo, ser� usado /home/username/transparencia/)
4. ln -s /var/www/dados/ /home/username/transparencia/resultado

Execu��o:
=========
- Sempre que quiser gerar novos dados, execute /home/username/transparencia/runEverything.py

