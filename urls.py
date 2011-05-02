from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(settings.PROJECT_NAME + '.core.views',
  url(r'^$', 'index', name='index'),
  url(r'^core/submit/(?P<img_id>\d+)', 'submit', name='vote_submit'),
  url(r'^core/upload', 'upload', name='img_upload'),
  url(r'^ajax', 'ajax', name='ajax'),
)

urlpatterns += patterns(settings.PROJECT_NAME + '.nav.views',
  url(r'^about$', 'about', name='about'),
  url(r'^news$', 'news', name='news'),
)

urlpatterns += patterns('',
  url(r'^notifier/updates$', settings.PROJECT_NAME + '.notifier.views.updates'),
)

urlpatterns += patterns('',
  (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
  (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
  (r'^admin/', include(admin.site.urls)),
)
