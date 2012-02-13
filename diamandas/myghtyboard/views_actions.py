#!/usr/bin/python
# Diamanda Application Set
# myghtyboard forum
# views that alter forum tables like delete, solve/move topic

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from diamandas.myghtyboard.models import *
from diamandas.myghtyboard.context import forum as forumContext
from diamandas.myghtyboard.utils import *

def delete_post(request, post_id, topic_id):
	"""
	delete a post
	
	* post_id - ID of a Post entry
	* topic_id - Topic entry ID that contain the Post entry
	"""
	try:
		topic = Topic.objects.get(id=topic_id)
		request.forum_id = topic.forum.id
		perms = forumContext(request)
	except:
		return HttpResponseRedirect(reverse('diamandas.myghtyboard.views.category_list', kwargs={}))
	
	if perms['perms']['is_staff']:
		Post.objects.get(id=post_id).delete()
		topic.posts = topic.posts -1
		if topic.posts > 0:
			topic.save()
			return redirect_by_template(request, reverse('diamandas.myghtyboard.views.post_list', kwargs={'pagination_id': 1, 'topic_id': topic_id}), _('Post deleted succesfuly.'))
		else:
			fid = topic.forum.id
			topic.delete()
			return redirect_by_template(request, reverse('diamandas.myghtyboard.views.topic_list', kwargs={'forum_id': fid}), _('Topic deleted succesfuly.'))
	else:
		return render_to_response('bug.html', {'bug': _('You aren\'t a moderator')}, context_instance=RequestContext(request, forumContext(request)))


def delete_topic(request, topic_id, forum_id):
	"""
	delete a topic with all posts
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	request.forum_id = forum_id
	perms = forumContext(request)
	
	if perms['perms']['is_staff']:
		posts = Post.objects.filter(topic=topic_id).count()
		t = Topic.objects.get(id=topic_id)
		if t.forum.id != int(forum_id):
			return render_to_response('bug.html', {'bug': _('Invalid Forum/Topic')}, context_instance=RequestContext(request, forumContext(request)))
		t.delete()
		Post.objects.filter(topic=topic_id).delete()
		forum = Forum.objects.get(id=forum_id)
		forum.topics = forum.topics -1
		forum.posts = forum.posts - posts
		forum.save()
		return redirect_by_template(request, reverse('diamandas.myghtyboard.views.topic_list', kwargs={'forum_id': forum_id}), _('Topic deleted succesfuly.'))
	else:
		return render_to_response('bug.html', {'bug': _('You aren\'t a moderator')}, context_instance=RequestContext(request, forumContext(request)))


def move_topic(request, topic_id, forum_id):
	"""
	move topic
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	request.forum_id = forum_id
	perms = forumContext(request)
	
	if perms['perms']['is_staff']:
		if request.POST and len(request.POST['forum']) > 0:
			topic = Topic.objects.get(id=topic_id)
			topic.forum=Forum.objects.get(id=request.POST['forum'])
			topic.save()
			t = Topic(
				forum=Forum.objects.get(id=forum_id),
				name = topic.name,
				author = topic.author,
				posts = 0,
				lastposter = _('Topic Moved'),
				is_locked = True)
			t.save()
			p = Post(
				topic = t,
				text = _('This topic has been moved to another forum. To see the topic follow')
					 + ' [url=' + reverse('diamandas.myghtyboard.views.post_list', kwargs={'pagination_id': 1, 'topic_id': topic_id}) + ']' + _('this link') + '[/url]',
				author = _('Forum Staff'),
				ip = str(request.META['REMOTE_ADDR']))
			p.save()
			return redirect_by_template(request, reverse('diamandas.myghtyboard.views.topic_list', kwargs={'forum_id': forum_id}), _('Topic moved succesfuly.'))
		else:
			forums = Forum.objects.exclude(id=forum_id)
			topic = Topic.objects.get(id=topic_id)
			return render_to_response(
				'myghtyboard/move_topic.html',
				{'forums': forums, 'topic': topic},
				context_instance=RequestContext(request, forumContext(request)))
	else:
		return render_to_response('bug.html',
			{'bug': _('You aren\'t a moderator')},
			context_instance=RequestContext(request, forumContext(request))
			)


def close_topic(request, topic_id, forum_id):
	"""
	close topic
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	request.forum_id = forum_id
	perms = forumContext(request)
	
	if perms['perms']['is_staff']:
		topic = Topic.objects.get(id=topic_id)
		topic.is_locked=True
		topic.save()
		return redirect_by_template(request, reverse('diamandas.myghtyboard.views.topic_list', kwargs={'forum_id': forum_id}), _('Topic closed succesfuly.'))
	else:
		return render_to_response('bug.html', {'bug': _('You aren\'t a moderator')}, context_instance=RequestContext(request, forumContext(request)))


def open_topic(request, topic_id, forum_id):
	"""
	open topic
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	request.forum_id = forum_id
	perms = forumContext(request)
	
	if perms['perms']['is_staff']:
		topic = Topic.objects.get(id=topic_id)
		topic.is_locked=False
		topic.save()
		return redirect_by_template(request, reverse('diamandas.myghtyboard.views.topic_list', kwargs={'forum_id': forum_id}), _('Topic opened succesfuly.'))
	else:
		return render_to_response('bug.html',
			{'bug': _('You aren\'t a moderator and you aren\'t logged in')},
			context_instance=RequestContext(request, forumContext(request))
			)

def solve_topic(request, topic_id, forum_id):
	"""
	marks topic as solved
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	topic = Topic.objects.get(id=topic_id)
	request.forum_id = forum_id
	perms = forumContext(request)
	
	if perms['perms']['is_staff'] or perms['perms']['is_authenticated'] and topic.author == str(request.user):
		topic.is_solved=True
		topic.save()
		return redirect_by_template(request, reverse('diamandas.myghtyboard.views.topic_list', kwargs={'forum_id': forum_id}), _('Topic solved.'))
	else:
		return render_to_response('bug.html',
			{'bug': _('You aren\'t a moderator or topic author and you aren\'t logged in')},
			context_instance=RequestContext(request, forumContext(request))
			)

def unsolve_topic(request, topic_id, forum_id):
	"""
	marks topic as unsolved
	
	* topic_id - ID of a Topic entry
	* forum_id - ID of a Forum entry that contain the Topic entry
	"""
	topic = Topic.objects.get(id=topic_id)
	request.forum_id = forum_id
	perms = forumContext(request)
	
	if perms['perms']['is_staff'] or perms['perms']['is_authenticated'] and topic.author == str(request.user):
		topic.is_solved=False
		topic.save()
		return redirect_by_template(request, reverse('diamandas.myghtyboard.views.topic_list', kwargs={'forum_id': forum_id}), _('Topic unsolved.'))
	else:
		return render_to_response('bug.html',
			{'bug': _('You aren\'t a moderator or topic author and you aren\'t logged in')},
			context_instance=RequestContext(request, forumContext(request))
			)
