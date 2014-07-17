from django.conf.urls import patterns, url
from graphit import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='graphit.index'),
  url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='graphit.detail'),
)
