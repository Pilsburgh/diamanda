#!/usr/bin/python
# -*- coding: utf-8 -*-
# Diamanda Application Set
# User Panel

import django.contrib.auth.views
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

from diamandas.userpanel.models import *
from diamandas.userpanel.forms import *
from diamandas.myghtyboard.utils import *


def user_panel(request):
	"""
	main user panel
	"""
	return render_to_response('userpanel/panel.html', {}, context_instance=RequestContext(request))

def login_user(request):
	"""
	django.contrib.auth.views.login login view
	"""
	if not request.user.is_authenticated():
		return django.contrib.auth.views.login(request, template_name='userpanel/login.html')
	else:
		return HttpResponseRedirect("/user/")

def logout_then_login(request):
	"""
	django.contrib.auth.views.logout_then_login logout view
	"""
	return django.contrib.auth.views.logout_then_login(request, login_url = '/')

def register(request):
	"""
	User registration
	"""
	form =  RegisterForm()
	if request.POST:
		stripper = Stripper()
		data = request.POST.copy()
		data['login'] = stripper.strip(data['login'])
		data['email'] = stripper.strip(data['email'])
		
		if data['email'].count('bachtra') > 0:
			return HttpResponse('x')
		
		form = RegisterForm(data)
		
		if form.is_valid():
			data = form.cleaned_data
			try:
				user = User.objects.create_user(data['login'], data['email'], data['password1'])
			except Exception:
				data['reply'] = ''
				return render_to_response(
					'userpanel/register.html',
					{'token': t, 'form': form, 'question': captcha['question'], 'error': True},
					context_instance=RequestContext(request))
			else:
				user.save()
				user = authenticate(username=data['login'], password=data['password1'])
				if user is not None:
					login(request, user)
				return redirect_by_template(request, "/user/", _('Registration compleated. You have been logged in succesfuly.'))
		else:
			data['reply'] = ''
			if '__all__' in form.errors:
				if str(form.errors['__all__']).find(_('Incorrect answer')) != -1:
					form.errors['reply'] = [_('Incorrect answer'),]
				if str(form.errors['__all__']).find(_("Login already taken")) != -1:
					form.errors['login'] = [_("Login already taken"),]
				if str(form.errors['__all__']).find(_("Email already taken")) != -1:
					form.errors['email'] = [_("Email already taken"),]
				if str(form.errors['__all__']).find(_("Passwords do not match.")) != -1:
					form.errors['password1'] = [_("Passwords do not match."),]
			return render_to_response(
				'userpanel/register.html',
				{'form': form, 'error': True},
				context_instance=RequestContext(request))
	
	return render_to_response(
		'userpanel/register.html',
		{'form': form},
		context_instance=RequestContext(request))

@login_required
def edit_user_data(request):
	form = EditUserData(instance=request.user)
	if request.POST:
		form = EditUserData(request.POST, instance=request.user)
		if form.is_valid():
			form =form.save()
			return HttpResponseRedirect('/user/')
	return render_to_response(
		'userpanel/edit_user_data.html',
		{'form': form},
		context_instance=RequestContext(request))


