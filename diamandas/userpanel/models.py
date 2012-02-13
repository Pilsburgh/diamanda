#!/usr/bin/python
# -*- coding: utf-8 -*-
# Diamanda Application Set
# User Panel
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class Profile(models.Model):
	"""
	User Profile
	"""
	user = models.ForeignKey(User, unique=True)
	onsitedata = models.DateTimeField(auto_now=True, blank=True)
	last_visit = models.DateTimeField(blank=True, auto_now_add=True)
	def __str__(self):
		return str(self.user)
	def __unicode__(self):
		return unicode(self.user)
	def save(self, **kwargs):
		if self.pk:
			if not self.last_visit:
				self.last_visit = datetime.now()
			self.last_visit = self.onsitedata
			self.onsitedata = datetime.now()
		super(Profile, self).save(**kwargs)
