# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('diamandas.userpanel.views',
(r'^$', 'user_panel'),
(r'^register/$', 'register'),
(r'^login/$', 'login_user'),
(r'^logout/$', 'logout_then_login'),
(r'^edit/$', 'edit_user_data'),
)
