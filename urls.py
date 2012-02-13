from django.conf.urls.defaults import patterns, include, url
import os.path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'site_media')}), # change it or remove if not on dev server
(r'^forum/', include('diamandas.myghtyboard.URLconf')),
    (r'^user/', include('diamandas.userpanel.URLconf')),
(r'^/?$', 'diamandas.myghtyboard.views.category_list'),
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('',
(r'^user/password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name':'userpanel/password_reset_form.html', 'email_template_name':'userpanel/password_reset_email.html'}),
(r'^user/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name':'userpanel/password_reset_done.html'}),
(r'^user/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name':'userpanel/password_reset_confirm.html'}),
(r'^user/reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name':'userpanel/password_reset_complete.html'}),
)

urlpatterns += patterns('',
(r'^user/password_change/$', 'django.contrib.auth.views.password_change', {'template_name':'userpanel/password_change.html'}),
(r'^user/password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name':'userpanel/password_change_done.html'}),
)
