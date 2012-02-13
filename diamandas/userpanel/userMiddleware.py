#!/usr/bin/python
# -*- coding: utf-8 -*-
# Diamanda Application Set
# User Panel

from datetime import timedelta
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login

from diamandas.userpanel.models import *

class userMiddleware(object):
	"""
	Update user onsitedata when he is on site (to display "users online")
	"""
	def process_request(self, request):
		if request.user.is_authenticated():
			now = datetime.now()
			check_time = now - timedelta(minutes=10)
			if not request.session.__contains__('onsite') or request.session['onsite'] < check_time:
				request.session['onsite'] = now
				try:
					a = Profile.objects.get(user=request.user)
					a.save()
				except:
					a = Profile(user=request.user)
					a.save()
