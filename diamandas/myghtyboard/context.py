#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum
from datetime import datetime, timedelta

from django.conf import settings

from diamandas.myghtyboard.models import Forum, Post

def forum(request):
	"""
	Forum permissions context function
	
	Returns a dictionary containing all the perms for request.user
	"""
	perms = {}
	perms['add_topic'] = False
	perms['add_post'] = False
	perms['is_staff'] = False
	perms['is_authenticated'] = False
	perms['is_spam'] = False
	
	if request.user.is_authenticated():
		# logged in may add topics and posts
		perms['add_topic'] = True
		perms['add_post'] = True
		perms['is_authenticated'] = True
		perms['is_staff'] = request.user.is_staff
		# post limit for registered user
		if not request.user.is_staff and settings.FORUM_MAX_USER_POST_PER_HOUR > 0:
			check_date = datetime.now() - timedelta(hours=1)
			spam = Post.objects.filter(author_system=request.user, date__gt=check_date).count()
			if spam >= settings.FORUM_MAX_USER_POST_PER_HOUR:
				perms['add_topic'] = False
				perms['add_post'] = False

		# check if request.user is a moderator
		if hasattr(request, 'forum_id'):
			try:
				forum = Forum.objects.get(id=request.forum_id)
			except:
				pass
			else:
				if forum.use_moderators and request.user in forum.moderators.all():
					perms['add_topic'] = True
					perms['add_post'] = True
					perms['is_authenticated'] = True
					perms['is_staff'] = True
	# anonymous may post only if the forum allows that
	elif not request.user.is_authenticated() and hasattr(request, 'forum_id'):
		# check if forum allows posting for anonymous
		try:
			forum = Forum.objects.get(id=request.forum_id)
		except:
			pass
		else:
			if forum.allow_anonymous:
				check_date = datetime.now() - timedelta(hours=1)
				spam = Post.objects.filter(author_anonymous=True, date__gt=check_date).count()
				if spam < settings.FORUM_MAX_ANONYMOUS_POSTS_PER_HOUR:
					perms['add_topic'] = True
					perms['add_post'] = True
				else:
					perms['is_spam'] = True
	return {'perms': perms, 'on_forum': True}