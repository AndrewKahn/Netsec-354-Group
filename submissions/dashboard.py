from bottle import route, run, template
from datetime import datetime

@route('')
@route('/')
def index():
	file = open("submit.log") 
	lines = file.readlines()
	lines.reverse()

	names = ('Programming Languages', 'Generating Shellcode', 'Overflows (I)', 'Overflows (II)', 'Web Attacks', 'Firewall and IDS', 'Web Attacks Lab')
	ret = '<!DOCTYPE html>\n<html>\n<h2 style="text-align:center;">Submission Dashboard</h2>\n<table>\n'
	for i in range(7): 
		j = 0
		while lines[j][0] != str(i + 1): 
			j = j + 1
		if 'ok' in lines[j]:
			ret += '<tr class="green"><td>' + names[i] + '</td>'
			while j < len(lines) and not (lines[j][0] == str(i + 1) and 'ok' not in lines[j]): 
				j = j + 1
			if j < len(lines): 
				ret += '<td class="right">Last Failure: ' + (":".join(lines[j].split(":")[2:]))[:-1] + '</td>'
			ret += '</tr>\n'
		else: 
			ret += '<tr class="red"><td>' + names[i] + '</td> <td class="right">Last Failure: ' + (":".join(lines[j].split(":")[2:]))[:-1] + '</td></tr>\n' 
	
	ret += '</table>\n<style>.red{background-color:red;}.green{background-color:green;}.right{padding: 10px 125px 10px 125px;}td{border-top:1px solid black;border-bottom:1px solid black;padding: 10px 125px 10px 10px}</style>\n</html>'
	return ret

run(host='0.0.0.0', port=4567)
