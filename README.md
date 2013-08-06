Transparência
=============
- Cota Parlamentar - spiders/cota_atividade.py - Crawler de http://www.camara.gov.br/cota-parlamentar/ (suporta data de início, mas ainda não está sendo usado)
- Dados de deputados - spiders/dados_deputados.py - Crawler de http://www2.camara.leg.br/deputados/pesquisa
- Prestação de contas de campanha - spiders/prestacao_contas.py - Crawler de http://spce2010.tse.jus.br/spceweb.consulta.prestacaoconta2010/pesquisaCandidato.jsp
- Recursos humanos - spiders/recursos_humanos.py - http://www2.camara.leg.br/transparencia/recursos-humanos/quadro-remuneratorio/consulta-secretarios-parlamentares

Instalação sugerida:
====================
1. Coloque os arquivos do diretório www/ em um diretório acessível por HTTP (como exemplo, será usado /var/www/html)
2. Crie o diretório /var/www/dados (não acessível pelo httpd, mas com permissão para o usuário do httpd acessar): chown apache: /var/www/dados
3. Instale os outros arquivos no diretório desejado (como exemplo, será usado /home/username/transparencia/)
4. ln -s /var/www/dados/ /home/username/transparencia/resultado

Execução:
=========
- Sempre que quiser gerar novos dados, execute /home/username/transparencia/runEverything.py

