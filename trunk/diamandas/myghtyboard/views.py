# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from myghtyboard.models import *
from django.http import HttpResponseRedirect
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from stripogram import html2safehtml
from django.db.models import Q
from django.core import validators

# list permissions used in templates
def list_perms(request):
	perms = {}
	# and request.user.has_perm('myghtyboard.add_topic')
	if request.user.is_authenticated():
		perms['add_topic'] = True
	else:
		perms['add_topic'] = False
	# and request.user.has_perm('myghtyboard.add_post')
	if request.user.is_authenticated():
		perms['add_post'] = True
	else:
		perms['add_post'] = False
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			perms['is_staff'] = True
		else:
			perms['is_staff'] = False
	else:
		perms['is_staff'] = False
	if request.user.is_authenticated():
		perms['is_authenticated'] = True
	return perms

# show all categories and their topics
def category_list(request):
	categories = Category.objects.all().order_by('cat_order')
	for c in categories:
		c.forums = c.forum_set.all().order_by('forum_order')
	
	return render_to_response('myghtyboard/category_list.html', {'categories': categories, 'perms': list_perms(request), 'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID})

# list of topics in a forum
def topic_list(request, forum_id):
	try:
		topics = Topic.objects.order_by('-is_global', '-is_sticky', '-topic_modification_date').filter(Q(topic_forum=forum_id) | Q(is_global='1'))
		for i in topics:
			pmax =  i.post_set.all().count()/10
			pmaxten =  i.post_set.all().count()%10
			if pmaxten != 0:
				i.pagination_max = pmax+1
			else:
				i.pagination_max = pmax
		forum_name = Forum.objects.get(id=forum_id)
		forum_name = forum_name.forum_name
	except:
		return HttpResponseRedirect('/forum/')
	return render_to_response('myghtyboard/topics_list.html', {'topics': topics, 'forum': forum_id,  'perms': list_perms(request), 'forum_name': forum_name, 'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID})


# list my topics
def my_topic_list(request, show_user=False):
	if not show_user:
		show_user = str(request.user)
	if request.user.is_authenticated():
		topics = Topic.objects.order_by('-topic_modification_date').filter(topic_author=show_user)[:50]
		for i in topics:
			pmax =  i.post_set.all().count()/10
			pmaxten =  i.post_set.all().count()%10
			if pmaxten != 0:
				i.pagination_max = pmax+1
			else:
				i.pagination_max = pmax
		forum_name = _('User Topics')
		return render_to_response('myghtyboard/mytopics_list.html', {'topics': topics, 'forum_name': forum_name, 'perms': list_perms(request), 'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID})
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t logged in'), 'sid': settings.SITE_ID}) # can't add topic


# list last active topics
def last_topic_list(request):
	if request.user.is_authenticated():
		topics = Topic.objects.order_by('-topic_modification_date')[:50]
		for i in topics:
			pmax =  i.post_set.all().count()/10
			pmaxten =  i.post_set.all().count()%10
			if pmaxten != 0:
				i.pagination_max = pmax+1
			else:
				i.pagination_max = pmax
		forum_name = _('Last Active Topics')
		return render_to_response('myghtyboard/mytopics_list.html', {'topics': topics, 'forum_name': forum_name, 'perms': list_perms(request), 'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID})
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t logged in'), 'sid': settings.SITE_ID}) # can't add topic


# list topics with my posts
def my_posttopic_list(request, show_user=False):
	if not show_user:
		show_user = str(request.user)
	if request.user.is_authenticated():
		try:
			topics = Post.objects.order_by('-post_date').filter(post_author=show_user).values('post_topic').distinct()[:50]
			posts = []
			for i in topics:
				posts.append(int(i['post_topic']))
			topics = Topic.objects.order_by('-topic_modification_date').filter(id__in=posts)
			for i in topics:
				pmax =  i.post_set.all().count()/10
				pmaxten =  i.post_set.all().count()%10
				if pmaxten != 0:
					i.pagination_max = pmax+1
				else:
					i.pagination_max = pmax
			forum_name = _('User Posts in Latest Topics')
		except:
			return render_to_response('myghtyboard/mytopics_list.html', {'perms': list_perms(request), 'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID})
		return render_to_response('myghtyboard/mytopics_list.html', {'topics': topics, 'forum_name': forum_name, 'perms': list_perms(request), 'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID})
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t logged in'), 'sid': settings.SITE_ID}) # can't add topic


# list post in topic with a generic pagination view :)
def post_list(request, topic_id, pagination_id):
	from django.views.generic.list_detail import object_list
	try:
		topic = Topic.objects.get(id=topic_id)
	except Topic.DoesNotExist:
		return HttpResponseRedirect('/forum/')
	if  topic.is_locked:
		opened = False
	else:
		opened = True
	return object_list(request, topic.post_set.all().order_by('post_date'), paginate_by = 10, page = pagination_id, extra_context = {'topic_id':topic_id, 'opened': opened, 'topic': topic.topic_name, 'forum_id': topic.topic_forum.id, 'forum_name': topic.topic_forum, 'perms': list_perms(request), 'current_user': str(request.user), 'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID}, template_name = 'myghtyboard/post_list.html')

# add topic
def add_topic(request, forum_id):
	# can add_topic or anonymous ANONYMOUS_CAN_ADD_TOPIC
	if request.user.is_authenticated():
		manipulator = Topic.AddManipulator()
		if request.POST and len(request.POST.copy()['text']) > 1 and  len(request.POST.copy()['topic_name']) > 1:
			page_data = request.POST.copy()
			page_data['topic_author'] = str(request.user)
			from re import findall, MULTILINE
			import base64
			from datetime import datetime
			tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['text'], MULTILINE)
			for i in tags:
				page_data['text'] = page_data['text'].replace('[code]'+i+'[/code]', '[code]'+base64.encodestring(i)+'[/code]')
			page_data['text'] = html2safehtml(page_data['text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'cite', 'blockquote'))
			tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['text'], MULTILINE)
			for i in tags:
				page_data['text'] = page_data['text'].replace('[code]'+i+'[/code]', '[code]'+base64.decodestring(i)+'[/code]')
			text = page_data['text']
			del page_data['text']
			page_data['topic_forum'] = forum_id
			page_data['topic_posts'] = 1
			page_data['topic_lastpost'] = str(request.user)+'<br />' + str(datetime.today())[:-7]
			manipulator.do_html2python(page_data)
			new_place = manipulator.save(page_data)
			post = Post(post_topic = new_place, post_text = text, post_author = str(request.user), post_ip = request.META['REMOTE_ADDR'])
			post.save()
			forum = Forum.objects.get(id=forum_id)
			forum.forum_topics = forum.forum_topics +1
			forum.forum_posts = forum.forum_posts +1
			forum.forum_lastpost = str(request.user)+' (' + str(datetime.today())[:-7] + ')<br /><a href="/forum/topic/1/' + str(new_place.id) + '/">' + str(new_place.topic_name) + '</a>'
			forum.save()
			
			from django.contrib.sites.models import Site
			from django.core.mail import mail_admins
			s = Site.objects.get(id=settings.SITE_ID)
			mail_admins('Temat Dodany', "Dodano Temat: http://www." + str(s) + "/forum/forum/" + forum_id +"/", fail_silently=True)
			
			return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
		else:
			errors = {}
			page_data = {}
		
		form = forms.FormWrapper(manipulator, page_data, errors)
		return render_to_response('myghtyboard/add_topic.html', {'form': form, 'perms': list_perms(request), 'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID})
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You can\'t add topics'), 'sid': settings.SITE_ID}) # can't add topic


# add post
def add_post(request, topic_id, post_id = False):
	# can add_post or anonymous ANONYMOUS_CAN_ADD_POST
	if request.user.is_authenticated():
		topic = Topic.objects.values('is_locked').get(id=topic_id)
		if topic['is_locked']:
			return render_to_response('myghtyboard/noperm.html', {'why': _('Topic is closed'), 'sid': settings.SITE_ID}) # locked topic!
		# check who made the last post.
		lastpost = Post.objects.order_by('-post_date').filter(post_topic=topic_id)[:1]
		if request.user.is_authenticated():
			user_data = User.objects.get(username=str(request.user))
			is_staff = user_data.is_staff
		else:
			is_staff = False
		# if the last poster is the current one (login) and he isn't staff then we don't let him post after his post
		if str(lastpost[0].post_author) == str(request.user) and not is_staff:
			return render_to_response('myghtyboard/noperm.html', {'why': _('You can\'t post after your post'), 'sid': settings.SITE_ID}) # can't post after post!
		else:
			manipulator = Post.AddManipulator()
			if request.POST and len(request.POST.copy()['post_text']) > 1:
				page_data = request.POST.copy()
				page_data['post_author'] = str(request.user)
				from re import findall, MULTILINE
				import base64
				from datetime import datetime
				tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['post_text'], MULTILINE)
				for i in tags:
					page_data['post_text'] = page_data['post_text'].replace('[code]'+i+'[/code]', '[code]'+base64.encodestring(i)+'[/code]')
				page_data['post_text'] = html2safehtml(page_data['post_text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'cite', 'blockquote'))
				tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['post_text'], MULTILINE)
				for i in tags:
					page_data['post_text'] = page_data['post_text'].replace('[code]'+i+'[/code]', '[code]'+base64.decodestring(i)+'[/code]')
				
				page_data['post_ip'] = request.META['REMOTE_ADDR']
				page_data['post_topic'] = topic_id
				manipulator.do_html2python(page_data)
				new_place = manipulator.save(page_data)
				
				topic = Topic.objects.get(id=topic_id)
				topic.topic_posts = topic.topic_posts +1
				topic.topic_lastpost = str(request.user)+'<br />' + str(datetime.today())[:-7]
				topic.save()
				
				forum = Forum.objects.get(id=topic.topic_forum.id)
				forum.forum_posts = forum.forum_posts +1
				
				pmax = Post.objects.filter(post_topic=topic_id).count()/10
				pmaxten =  Post.objects.filter(post_topic=topic_id).count()%10
				if pmaxten != 0:
					pmax = pmax+1
				
				forum.forum_lastpost = str(request.user)+' (' + str(datetime.today())[:-7] + ')<br /><a href="/forum/topic/' + str(pmax) + '/' + str(topic.id) + '/">' + str(topic.topic_name) + '</a>'
				forum.save()
				
				from django.contrib.sites.models import Site
				from django.core.mail import mail_admins
				s = Site.objects.get(id=settings.SITE_ID)
				mail_admins('Post Dodany', "Dodano Post: http://www." + str(s) + "/forum/topic/" + str(pmax) + "/" + topic_id +"/", fail_silently=True)
				
				return HttpResponseRedirect("/forum/topic/" + str(pmax) + "/" + topic_id +"/")
			else:
				if post_id:
					quote = Post.objects.get(id=post_id)
					quote_text = '<blockquote><b>' + quote.post_author + ' wrote:</b><br /><cite>' + quote.post_text + '</cite></blockquote>\n'
				else:
					quote_text = ''
			# get 10 last posts from this topic
			lastpost = Post.objects.filter(post_topic=topic_id).order_by('-id')[:10]
			return render_to_response('myghtyboard/add_post.html', {'quote_text': quote_text, 'lastpost': lastpost, 'perms': list_perms(request), 'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID})
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You can\'t add posts'), 'sid': settings.SITE_ID}) # can't add posts

#edit post
def edit_post(request, post_id):
	post = Post.objects.get(id=post_id)
	topic = Topic.objects.values('is_locked').get(id=post.post_topic.id)
	if topic['is_locked']:
		return render_to_response('myghtyboard/noperm.html', {'why': _('Topic is closed'), 'sid': settings.SITE_ID}) # locked topic!
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		is_staff = user_data.is_staff
	else:
		is_staff = False

	# if the editor is the post author or is he a staff member
	if str(request.user) == post.post_author and request.user.is_authenticated() or  is_staff:
		if request.POST and len(request.POST.copy()['post_text']) > 1:
			page_data = request.POST.copy()
			from re import findall, MULTILINE
			import base64
			from datetime import datetime
			tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['post_text'], MULTILINE)
			for i in tags:
				page_data['post_text'] = page_data['post_text'].replace('[code]'+i+'[/code]', '[code]'+base64.encodestring(i)+'[/code]')
			page_data['post_text'] = html2safehtml(page_data['post_text'] ,valid_tags=('b', 'a', 'i', 'br', 'p', 'u', 'img', 'li', 'ul', 'ol', 'center', 'sub', 'sup', 'cite', 'blockquote'))
			tags = findall( r'(?xs)\[code\](.*?)\[/code\]''', page_data['post_text'], MULTILINE)
			for i in tags:
				page_data['post_text'] = page_data['post_text'].replace('[code]'+i+'[/code]', '[code]'+base64.decodestring(i)+'[/code]')
			post.post_text = page_data['post_text']
			post.save()
			
			pmax = Post.objects.filter(post_topic=post.post_topic).count()/10
			pmaxten =  Post.objects.filter(post_topic=post.post_topic).count()%10
			if pmaxten != 0:
				pmax = pmax+1
			return HttpResponseRedirect("/forum/topic/" + str(pmax) + "/" + str(post.post_topic.id) +"/")
		else:
			return render_to_response('myghtyboard/edit_post.html', {'post_text': post.post_text, 'perms': list_perms(request), 'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID})
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You can\'t edit this post'), 'sid': settings.SITE_ID}) # can't edit post

# delete a post
def delete_post(request, post_id, topic_id):
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			Post.objects.get(id=post_id).delete()
			topic = Topic.objects.get(id=topic_id)
			topic.topic_posts = topic.topic_posts -1
			topic.save()
			return HttpResponseRedirect("/forum/topic/1/" + topic_id +"/")
		else:
			return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator'), 'sid': settings.SITE_ID}) # can't delete
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in'), 'sid': settings.SITE_ID}) # can't delete

# delete a topic with all posts
def delete_topic(request, topic_id, forum_id):
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			posts = Post.objects.filter(post_topic=topic_id).count()
			Topic.objects.get(id=topic_id).delete()
			Post.objects.filter(post_topic=topic_id).delete()
			forum = Forum.objects.get(id=forum_id)
			forum.forum_topics = forum.forum_topics -1
			forum.forum_posts = forum.forum_posts - posts
			forum.save()
			return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
		else:
			return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator'), 'sid': settings.SITE_ID}) # can't delete
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in'), 'sid': settings.SITE_ID}) # can't delete

# move topic
def move_topic(request, topic_id, forum_id):
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			if request.POST and len(request.POST['forum']) > 0:
				topic = Topic.objects.get(id=topic_id)
				topic.topic_forum=Forum.objects.get(id=request.POST['forum'])
				topic.save()
				t = Topic(topic_forum=Forum.objects.get(id=forum_id), topic_name = topic.topic_name, topic_author = topic.topic_author, topic_posts = 0, topic_lastpost = _('Topic Moved'), is_locked = True)
				t.save()
				p = Post(post_topic = t, post_text = _('This topic has been moved to another forum. To see the topic follow') + ' <a href="/forum/topic/1/' + str(topic_id) +'/"><b>' + _('this link') + '</b></a>', post_author = _('Forum Staff'), post_ip = str(request.META['REMOTE_ADDR']))
				p.save()
				return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
			else:
				forums = Forum.objects.exclude(id=forum_id)
				topic = Topic.objects.get(id=topic_id)
				return render_to_response('myghtyboard/move_topic.html', {'forums': forums, 'topic': topic, 'perms': list_perms(request), 'site_name':settings.SITE_NAME, 'sid': settings.SITE_ID})
		else:
			return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator'), 'sid': settings.SITE_ID}) # can't move
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in'), 'sid': settings.SITE_ID}) # can't move

# close topic
def close_topic(request, topic_id, forum_id):
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			topic = Topic.objects.get(id=topic_id)
			topic.is_locked=True
			topic.save()
			return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
		else:
			return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator'), 'sid': settings.SITE_ID}) # can't close
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in'), 'sid': settings.SITE_ID}) # can't close

# open topic
def open_topic(request, topic_id, forum_id):
	if request.user.is_authenticated():
		user_data = User.objects.get(username=str(request.user))
		if user_data.is_staff:
			topic = Topic.objects.get(id=topic_id)
			topic.is_locked=False
			topic.save()
			return HttpResponseRedirect("/forum/forum/" + forum_id +"/")
		else:
			return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator'), 'sid': settings.SITE_ID}) # can't open
	else:
		return render_to_response('myghtyboard/noperm.html', {'why': _('You aren\'t a moderator and you aren\'t logged in'), 'sid': settings.SITE_ID}) # can't open
