#!/usr/bin/python
# Diamanda Application Set
# Pages module

from datetime import datetime, timedelta

from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django import newforms as forms

from boxcomments.models import Comment
from pages.models import *
from userpanel.models import Profile
from myghtyboard.models import Topic

def show_index(request):
	"""
	Show the main page
	"""
	itopics = Topic.objects.all().values('id', 'name', 'last_pagination_page', 'lastposter').order_by('-modification_date')[:4]
	entries = Content.objects.all().values(
		'id', 'slug', 'date', 'title', 'parsed_description',
		'comments_count', 'current_book', 'current_book_title',
		'is_update', 'changes', 'content_type').order_by('-date')[:5]
	com = Comment.objects.order_by('-id')[:4]
	now = datetime.now()
	check_time = now - timedelta(minutes=10)
	onsite = Profile.objects.select_related().filter(onsitedata__gt=check_time).order_by('-onsitedata')[:4]
	return render_to_response(
		'pages/show_index.html',
		{'entries': entries, 'itopics': itopics, 'com': com, 'onsite': onsite, 'home_text': settings.HOME_TEXT},
		context_instance=RequestContext(request))

def list_news(request, book=False):
	"""
	List news
	
	* book - slug of a Content entry (book content_type)
	"""
	if book:
		bk = Content.objects.get(slug=book)
		news = Content.objects.filter(content_type='news', place=bk).order_by('-date')
		return object_list(
			request,
			news,
			paginate_by = 10,
			allow_empty = True,
			template_name = 'pages/news_list.html',
			extra_context = {'book': book, 'bk':bk, 'current_book': bk.slug})
	else:
		news = Content.objects.filter(content_type='news').order_by('-date').values('slug', 'title', 'date')
	return object_list(
		request,
		news,
		paginate_by = 10,
		allow_empty = True,
		template_name = 'pages/news_list.html',
		extra_context = {'book': book})

def show(request, slug):
	"""
	show Content entry
	
	* slug - slug of a Content entry
	"""
	try:
		page = Content.objects.filter(slug=slug).values(
			'id', 'slug', 'date', 'title', 'parsed_description', 'description',
			'parsed_text', 'comments_count', 'current_book', 'crumb', 'content_type')
	except Content.DoesNotExist:
		return render_to_response('pages/bug.html',
			{'bug': _('Page does not exist')},
			context_instance=RequestContext(request))
	page = page[0]
	if page['content_type'] == 'news':
		return render_to_response(
			'pages/show_news.html',
			{'page': page},
			context_instance=RequestContext(request, {'current_book': page['current_book']}))
	return render_to_response(
		'pages/show.html',
		{'page': page},
		context_instance=RequestContext(request, {'current_book': page['current_book']}))

def sitemap(request):
	"""
	Sitemap generator
	"""
	pages = Content.objects.values('slug', 'date', 'content_type')
	for p in pages:
		p['date'] = str(p['date'])[0:10]
	return render_to_response('pages/sitemap.html', {'pages': pages}, context_instance=RequestContext(request))

def full_rss(request):
	"""
	RSS channel
	"""
	pages = Content.objects.all().values('slug', 'title', 'parsed_description', 'date', 'content_type').order_by('-id')[:10]
	return render_to_response('pages/rss2.html', {'pages': pages}, context_instance=RequestContext(request))

def book_rss(request, slug):
	"""
	RSS channel for a book
	
	* book - slug of a Content entry (book content_type)
	"""
	book = Content.objects.get(slug=slug)
	pages = Content.objects.all().filter(place=book).values('slug', 'title',
		'parsed_description', 'date', 'content_type').order_by('-id')[:10]
	return render_to_response('pages/rss1.html', {'pages': pages, 'book': book}, context_instance=RequestContext(request))

def search_pages(request):
	"""
	Search view
	"""
	if request.POST:
		data = request.POST.copy()
		return render_to_response(
			'pages/search.html',
			{'term': data['term'], 'key': settings.GOOGLE_AJAX_SEARCH_API_KEY},
			context_instance=RequestContext(request)
			)
	else:
		return render_to_response('pages/search.html', {'key': key}, context_instance=RequestContext(request))
