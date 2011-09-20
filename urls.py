from django.conf.urls.defaults import *
from blog import views
from blog.feeds import LatestEntries

urlpatterns = patterns('',
	url(r'^$', views.index, name='blog_index'),
	url(r'^(?P<year>\d{4})/$', views.entries_by_year, name='blog_entries_by_year'),
	url(r'^(?P<year>\d{4})/(?P<slug>[\w\-]+)/$', views.entry_detail, name='blog_entry_detail'),
	url(r'^(?P<year>\d{4})/(?P<slug>[\w\-]+)/preview/$', views.entry_preview, name='blog_entry_preview'),
	url(r'^tag/(?P<tag>[a-zA-Z0-9\.\-+/ ]+)/$', views.entries_by_tag, name='blog_entries_by_tag'),
	url(r'^feed/$', LatestEntries(), name='blog_feed'),
)