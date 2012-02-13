#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum
# functions that wrap permission checks

from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response
from django.template import RequestContext

from diamandas.myghtyboard.context import forum as forumContext

def cant_add_topic(request):
	perms = forumContext(request)
	if not perms['perms']['add_topic'] and not perms['perms']['is_spam']:
		return render_to_response('pages/bug.html',
			{'bug': _('You can\'t add a topic.')},
			context_instance=RequestContext(request, perms)
			)
	if not perms['perms']['add_topic'] and perms['perms']['is_spam']:
		return render_to_response('pages/bug.html',
			{'bug': _('To many anonymous posts. Login to post topics and new messages.')},
			context_instance=RequestContext(request, perms)
			)
	return False

def cant_add_post(request, topic_is_locked):
	perms = forumContext(request)
	if not perms['perms']['add_post'] and not perms['perms']['is_spam']:
		return render_to_response('pages/bug.html',
			{'bug': _('You can\'t add a post.')},
			context_instance=RequestContext(request, perms)
			)
	if not perms['perms']['add_post'] and perms['perms']['is_spam']:
		return render_to_response('pages/bug.html',
			{'bug': _('To many anonymous posts. Login to post topics and new messages.')},
			context_instance=RequestContext(request, perms)
			)
	if topic_is_locked:
		return render_to_response('pages/bug.html', {'bug': _('Topic is closed')}, context_instance=RequestContext(request, perms))
	return False

def cant_edit_post(request, topic_is_locked, post_author):
	perms = forumContext(request)
	if str(request.user) != post_author and not perms['perms']['is_staff']:
		return render_to_response('pages/bug.html',
			{'bug': _('You can\'t edit a post.')},
			context_instance=RequestContext(request, perms)
			)
	if topic_is_locked:
		return render_to_response('pages/bug.html',
			{'bug': _('Topic is closed')},
			context_instance=RequestContext(request, perms)
			)
	return False