from django.conf.urls import patterns, url
from graphit_admin import views

urlpatterns = patterns('',
	url(r'^$', views.new, name='graphit_admin.index'),
)
