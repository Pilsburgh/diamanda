# -*- coding: utf-8 -*-
#!/usr/bin/python
# Diamanda Application Set
# Utils
import sgmllib
from re import compile 

from django.shortcuts import render_to_response
from django.template import RequestContext

def redirect_by_template(request, redirect_to, msg):
	return render_to_response('msg.html', {'msg': msg, 'redirect_to': redirect_to}, context_instance=RequestContext(request))

class Stripper(sgmllib.SGMLParser):
	"""
	Strip HTML tags from a string
	
	stripper = Stripper()
	print stripper.strip("text")
	"""
	def __init__(self):
		sgmllib.SGMLParser.__init__(self)
		
	def strip(self, some_html):
		self.theString = ""
		self.feed(some_html)
		self.close()
		r = compile('<.*?>|\&.*?\;')
		self.theString = r.sub("", self.theString)
		return self.theString
		
	def handle_data(self, data):
		self.theString += data
