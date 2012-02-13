from django.conf.urls.defaults import *

# Myghtyboard URLs
urlpatterns = patterns('diamandas.myghtyboard.views',
(r'^$', 'category_list'),
(r'^forum/(?P<forum_id>[0-9]+)/$', 'topic_list'),
(r'^forum/(?P<forum_id>[0-9]+)/(?P<pagination_id>[0-9]+)/$', 'topic_list'),
(r'^topic/(?P<pagination_id>[0-9]+)/(?P<topic_id>[0-9]+)/$', 'post_list'),
(r'^mytopics/(?P<show_user>.*)/$', 'my_topic_list'),
(r'^mytopics/$', 'my_topic_list'),
(r'^lasttopics/$', 'last_topic_list'),
(r'^myptopics/(?P<show_user>.*)/$', 'my_posttopic_list'),
(r'^myptopics/$', 'my_posttopic_list'),
)

urlpatterns += patterns('diamandas.myghtyboard.views_add_edit',
(r'^add_topic/(?P<forum_id>[0-9]+)/$', 'add_topic'),
(r'^add_post/(?P<topic_id>[0-9]+)/(?P<post_id>[0-9]+)/$', 'add_post'), # add post with quote
(r'^add_post/(?P<topic_id>[0-9]+)/$', 'add_post'),
(r'^edit_post/(?P<post_id>[0-9]+)/$', 'edit_post'),
)

urlpatterns += patterns('diamandas.myghtyboard.views_actions',
(r'^delete_post/(?P<post_id>[0-9]+)/(?P<topic_id>[0-9]+)/$', 'delete_post'),
(r'^move_topic/(?P<topic_id>[0-9]+)/(?P<forum_id>[0-9]+)/$', 'move_topic'),
(r'^delete_topic/(?P<topic_id>[0-9]+)/(?P<forum_id>[0-9]+)/$', 'delete_topic'),
(r'^close_topic/(?P<topic_id>[0-9]+)/(?P<forum_id>[0-9]+)/$', 'close_topic'),
(r'^open_topic/(?P<topic_id>[0-9]+)/(?P<forum_id>[0-9]+)/$', 'open_topic'),
(r'^topic/solve/(?P<topic_id>[0-9]+)/(?P<forum_id>[0-9]+)/$', 'solve_topic'),
(r'^topic/unsolve/(?P<topic_id>[0-9]+)/(?P<forum_id>[0-9]+)/$', 'unsolve_topic'),
)