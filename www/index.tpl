<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8">
<title>Dados</title>
</head>
<body>
<table border="1">
<tr>
<td>Arquivo</td>
<td>Última atualização</td>
</tr>
{% for item in items %}
<tr>
<td>{{ item['desc'] }}</td>
<td>{% if item['lastUpdate'] != None %}{{ item['lastUpdate'].strftime('%d/%m/%Y %H:%M:%S') }}{% endif %}</td>
{% for format in item['formats'] %}
<td>{% if format.values()[0] != None %}<a href="/dados.py?filename={{ item['filename'] }}&format={{ format.keys()[0] }}">{% endif %}{{ format.keys()[0] }}{% if format.values()[0] != None %} ({{ '%.1f'|format(format.values()[0]) }} MBs)</a>{% endif %}</td>
{% endfor %}
</tr>
{% endfor %}
</table>
</body>
</html>
