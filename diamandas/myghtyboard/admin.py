# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _

from diamandas.myghtyboard.models import *

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name','order')

class ForumAdmin(admin.ModelAdmin):
        list_display = ('name', 'description', 'category', 'prefixes', 'order')
	fieldsets = (
		(_('Data'), {
		'fields': ('category', 'name', 'description', 'order', 'use_moderators', 'moderators', 'use_prefixes', 'allow_anonymous')
		}),
		(_('Stats'), {'fields': ('topics', 'posts'), 'classes': ('collapse',)}),
		('', {'fields': ('lastposter', 'lasttopic', ), 'classes': ('collapse', 'wide')}),)
	


class PrefixAdmin(admin.ModelAdmin):
	list_display = ('name', 'list_forums')
	
admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Prefix, PrefixAdmin)
