#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum

from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class Category(models.Model):
	"""
	Categories that contain forums
	"""
	name = models.CharField(max_length=255, verbose_name=_("Category Name"))
	order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Order"))
	class Meta:
		verbose_name = _("Category")
		verbose_name_plural = _("1. Categories")
		db_table = 'rk_category' + str(settings.SITE_ID)
	def __str__(self):
		return self.name
	def __unicode__(self):
		return self.name

class Forum(models.Model):
	"""
	A forum model
	"""
	category = models.ForeignKey(Category, verbose_name=_("Forum Category"))
	name = models.CharField(max_length=255, verbose_name=_("Forum Name"))
	description = models.CharField(max_length=255, verbose_name=_("Forum Description"))
	topics = models.PositiveIntegerField(blank=True,default=0, verbose_name=_("Topics"))
	posts = models.PositiveIntegerField(blank=True,default=0, verbose_name=_("Posts"))
	lastposter = models.CharField(max_length=255, verbose_name=_("Last Poster"), blank=True, default='', null=True)
	lasttopic = models.CharField(max_length=255, verbose_name=_("Last Topic"), blank=True, default='', null=True)
	modification_date = models.DateTimeField(auto_now=True, blank=True)
	order = models.PositiveSmallIntegerField(default=0)
	use_prefixes = models.BooleanField(blank=True, default=False, verbose_name=_('Use prefixes'))
	allow_anonymous = models.BooleanField(blank=True, default=False, verbose_name=_('Allow anonymous to post'))
	use_moderators = models.BooleanField(blank=True, default=False, verbose_name=_('Use moderators'))
	moderators = models.ManyToManyField(User, verbose_name=_('Moderators'), blank=True, null=True,
		help_text=_('Select non-staff users that should be moderators of this forum (optional).'), limit_choices_to={'is_staff': False}
		)
	class Meta:
		verbose_name = _("Forum")
		verbose_name_plural = _("2. Forums")
		db_table = 'rk_forum' + str(settings.SITE_ID)
	def __str__(self):
		return self.name
	def __unicode__(self):
		return self.name
	def prefixes(self):
		if self.use_prefixes:
			p = Prefix.objects.filter(forums=self)
			pr = False
			if len(p) > 0:
				for i in p:
					if not pr:
						pr = i
					else:
						pr = '%s, %s' % (pr, i)
				return pr
			else:
				return '<a href="/admin/myghtyboard/prefix/">%s</a>' % _('No prefixes specified')
		else:
			return _('Not used')
	prefixes.allow_tags = True
	prefixes.short_description = _('Prefixes')

class Topic(models.Model):
	"""
	Model for topics in forums
	"""
	forum = models.ForeignKey(Forum, verbose_name=_("Forum"))
	name = models.CharField(max_length=255, verbose_name=_("Topic Title"))
	prefixes = models.CharField(max_length=255, verbose_name=_("Prefixes"), blank=True)
	author = models.CharField(max_length=255, verbose_name=_("Author"), blank=True)
	author_anonymous = models.BooleanField(blank=True, default=False)
	author_system = models.ForeignKey(User, blank=True, null=True)
	posts = models.PositiveIntegerField(default=0, blank=True, verbose_name=_("Posts"))
	lastposter = models.CharField(max_length=255, verbose_name=_("Last Poster"))
	modification_date = models.DateTimeField(default=datetime.now())
	last_pagination_page = models.PositiveIntegerField(default=1, blank=True, verbose_name=_("Pagination Page"))
	is_sticky = models.BooleanField(blank=True, default=False)
	is_locked = models.BooleanField(blank=True, default=False)
	is_global = models.BooleanField(blank=True, default=False)
	is_solved = models.BooleanField(blank=True, default=False)
	is_external = models.BooleanField(blank=True, default=False)
	class Meta:
		verbose_name = _("Topic")
		verbose_name_plural = _("Topics")
		db_table = 'rk_topic' + str(settings.SITE_ID)
	def __str__(self):
		return self.name
	def __unicode__(self):
		return self.name
	def save(self, **kwargs):
		if self.pk and self.is_solved == False:
			self.modification_date = datetime.now()
		super(Topic, self).save(**kwargs)

class Prefix(models.Model):
	"""
	Model for setting topic prefixes for selected forums
	"""
	name = models.CharField(max_length=20, verbose_name=_("Name"))
	forums = models.ManyToManyField(Forum, verbose_name=_('Forums'))
	class Meta:
		verbose_name = _("Topic Prefix")
		verbose_name_plural = _("3. Topic Prefixes")
		db_table = 'rk_prefix' + str(settings.SITE_ID)
	def __str__(self):
		return self.name
	def __unicode__(self):
		return self.name
	def list_forums(self):
		ret = False
		for i in self.forums.values():
			if not ret:
				ret = i['name']
			else:
				ret = '%s, %s' % (ret, i['name'])
		return ret
	list_forums.short_description = _('Forums')

class TopicPrefix(models.Model):
	"""
	Model for prefix - topic relation. Used in filtering topics by prefix
	"""
	topic = models.ForeignKey(Topic)
	prefix = models.ManyToManyField(Prefix)
	class Meta:
		db_table = 'rk_topicprefix' + str(settings.SITE_ID)

class Post(models.Model):
	"""
	Model for topic posts
	"""
	topic = models.ForeignKey(Topic)
	text = models.TextField()
	author = models.CharField(max_length=255, blank=True)
	author_anonymous = models.BooleanField(blank=True, default=False)
	author_system = models.ForeignKey(User, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	ip = models.CharField(max_length=20, blank=True)
	class Meta:
		verbose_name = _("Post")
		verbose_name_plural = _("Posts")
		db_table = 'rk_post' + str(settings.SITE_ID)
	def is_injected_post(self):
		if self.text.find(_('This is a discussion about article')) == -1:
			return False
		else:
			return True
	def __str__(self):
		return str(self.id)
	def __unicode__(self):
		return unicode(self.id)
