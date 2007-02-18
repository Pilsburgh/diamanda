from django.db import models

# Forum Categories
class Category(models.Model):
	cat_name = models.CharField(maxlength=255, verbose_name=_("Category Name")) # name of the category
	cat_order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Order")) # order of categories on the forum-categories list
	class Meta:
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")
	class Admin:
		list_display = ('cat_name','cat_order')
	def __str__(self):
		return self.cat_name

# Forums
class Forum(models.Model):
	forum_category = models.ForeignKey(Category, verbose_name=_("Forum Category")) # Forum category
	forum_name = models.CharField(maxlength=255, verbose_name=_("Forum Name")) # name of the forum
	forum_description = models.CharField(maxlength=255, verbose_name=_("Forum Description")) # desc of the forum
	forum_topics = models.PositiveIntegerField(default='0', blank=True, verbose_name=_("Topics")) # number of topics
	forum_posts = models.PositiveIntegerField(default='0', blank=True, verbose_name=_("Posts")) # number of posts
	forum_lastpost = models.CharField(maxlength=255, verbose_name=_("Last Post"), blank=True, default='', null=True) # last poster info etc.
	forum_order = models.PositiveSmallIntegerField(default=0) # order of forums on the category list
	class Meta:
		verbose_name = _("Forum")
		verbose_name_plural = _("Forums")
	class Admin:
		list_display = ('forum_name', 'forum_description', 'forum_category', 'forum_order')
		fields = (
		(None, {
		'fields': ('forum_category', 'forum_name', 'forum_description', 'forum_order', 'forum_topics', 'forum_posts')
		}),)
	def __str__(self):
		return self.forum_name

# Topics
class Topic(models.Model):
	topic_forum = models.ForeignKey(Forum, verbose_name=_("Forum")) # Forum of the topic
	topic_name = models.CharField(maxlength=255, verbose_name=_("Topic Title")) # name of the topic
	topic_author = models.CharField(maxlength=255, verbose_name=_("Author"), blank=True) # topic author
	topic_posts = models.PositiveIntegerField(default=0, blank=True, verbose_name=_("Posts")) # number of posts
	topic_lastpost = models.CharField(maxlength=255, verbose_name=_("Last Post")) # last poster etc.
	topic_modification_date = models.DateTimeField(auto_now = True) # last post date :)
	is_sticky = models.BooleanField(blank=True, default=False) # is a changeset a proposal - when user can't set it as a current ver.
	is_locked = models.BooleanField(blank=True, default=False) # is a changeset a proposal - when user can't set it as a current ver.
	is_global = models.BooleanField(blank=True, default=False) # is a changeset a proposal - when user can't set it as a current ver.
	class Meta:
		verbose_name = _("Topic")
		verbose_name_plural = _("Topics")
	def __str__(self):
		return self.topic_name

class Post(models.Model):
	post_topic = models.ForeignKey(Topic, verbose_name=_("Post")) # parent category if any
	post_text = models.TextField() # the post text
	post_author = models.CharField(maxlength=255, verbose_name=_("Author"), blank=True) # topic author
	post_date = models.DateTimeField(auto_now_add = True) # post add date
	post_ip = models.CharField(maxlength=20, blank=True)
	class Meta:
		verbose_name = _("Post")
		verbose_name_plural = _("Posts")
	def __str__(self):
		return str(self.id)
