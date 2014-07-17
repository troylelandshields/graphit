from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^graphit/', include('graphit.urls')),
    url(r'^graphit_admin/', include('graphit_admin.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/troyshields/Documents/Web/filegraph/media', "show_indexes":True}),
)
