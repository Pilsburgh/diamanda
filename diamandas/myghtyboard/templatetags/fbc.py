#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum

from re import findall
import base64

from pygments import highlight
from pygments.lexers import get_lexer_by_name,HtmlLexer
from pygments.formatters import HtmlFormatter

from django import template
from django.conf import settings

from diamandas.myghtyboard.utils import *

register = template.Library()

def fbc(value):
	"""
	Parse emotes, BBcode and format [code] blocks
	"""
	tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', value)
	for i in tags:
		j = base64.b64encode(i.encode('utf-8'))
		high = '[code]%s[/code]' % j
		value = value.replace('[code]%s[/code]' % i, high)
	
	tags = findall( r'(?xs)\[python\](.*?)\[/python\]''', value)
	for i in tags:
		j = base64.b64encode(i.encode('utf-8'))
		high = '[python]%s[/python]' % j
		value = value.replace('[python]%s[/python]' % i, high)
	
	tags = findall( r'(?xs)\[php\](.*?)\[/php\]''', value)
	for i in tags:
		j = base64.b64encode(i.encode('utf-8'))
		high = '[php]%s[/php]' % j
		value = value.replace('[php]%s[/php]' % i, high)
	
	stripper = Stripper()
	value = stripper.strip(value)
	value = value.replace('\n', '<br />')
	value = value.replace("'", '&#39;').replace('"', '&#34;')
	
	tags = findall( r'(?xs)\[url=(.*?)\](.*?)\[/url]''', value)
	for i in tags:
		value = value.replace('[url=%s]%s[/url]' % (i[0], i[1]), '<a href="%s">%s</a>' % (i[0].replace('"', ''), i[1]))
	
	value = value.replace('[b]', '<b>')
	value = value.replace('[/b]', '</b>')
	value = value.replace('[i]', '<i>')
	value = value.replace('[/i]', '</i>')
	value = value.replace('[u]', '<u>')
	value = value.replace('[/u]', '</u>')
	value = value.replace('[quote]', '<blockquote>')
	value = value.replace('[/quote]', '</blockquote>')
	value = value.replace('[url]', '')
	value = value.replace('[/url]', '')
	
	tags = findall( r'(?xs)\[img\](.*?)\[/img]''', value)
	for i in tags:
		if not len(i) < 3 and i[0:4] == 'http':
			value = value.replace('[img]%s[/img]' % i, '<img src="%s" alt="" />' % i)
	
	pygments_formatter = HtmlFormatter()
	
	lexer = get_lexer_by_name('html')
	tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', value)
	for i in tags:
		try:
			j = base64.b64decode(i).replace('<br />', '\n')
		except:
			j = ''
		high = '<div class="box" style="width:90%%;margin-left:auto;margin-right:auto;">%s</div>' % (highlight(j, lexer, pygments_formatter))
		value = value.replace('[code]%s[/code]' % i, high)
	
	lexer = get_lexer_by_name('python')
	tags = findall( r'(?xs)\[python\](.*?)\[/python\]''', value)
	for i in tags:
		try:
			j = base64.b64decode(i).replace('<br />', '\n')
		except:
			j = ''
		high = '<div class="box" style="width:90%%;margin-left:auto;margin-right:auto;">%s</div>' % (highlight(j, lexer, pygments_formatter))
		value = value.replace('[python]%s[/python]' % i, high)
	
	
	lexer = get_lexer_by_name('php')
	HtmlFormatter().get_style_defs('.highlight_php')
	tags = findall( r'(?xs)\[php\](.*?)\[/php\]''', value)
	for i in tags:
		try:
			j = base64.b64decode(i).replace('<br />', '\n')
		except:
			j = ''
		if j.find('<?php') < 1:
			j = '<?php\n%s' % j
		high = '<div class="box" style="width:90%%;margin-left:auto;margin-right:auto;">%s</div>' % (highlight(j, lexer, pygments_formatter))
		value = value.replace('[php]%s[/php]' % i, high)
	
	#value = value.replace(' :( ', '<img src="/site_media/layout/markitup/sets/bbcode/images/emoticon-unhappy.png" alt="" />')
	#value = value.replace(' :o ', '<img src="/site_media/layout/markitup/sets/bbcode/images/emoticon-surprised.png" alt="" />')
	#value = value.replace(' :p ', '<img src="/site_media/layout/markitup/sets/bbcode/images/emoticon-tongue.png" alt="" />')
	#value = value.replace(' ;) ', '<img src="/site_media/layout/markitup/sets/bbcode/images/emoticon-wink.png" alt="" />')
	#value = value.replace(' :D ', '<img src="/site_media/layout/markitup/sets/bbcode/images/emoticon-smile.png" alt="" />')

	return value

register.filter('fbc', fbc)
