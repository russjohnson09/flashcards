from django.conf.urls import patterns, include, url

from django.contrib import admin

import views
admin.autodiscover()

urlpatterns = patterns('',
    #main view. Displays user decks along with info on due dates, etc.
    url(r'^$', views.index, name='index'),

    url(r'^create/$', views.create, name='create'),
    url(r'^delete/$', views.delete, name='delete'),

    url(r'^(?P<blog_id>\w+)/$', views.blog_view, name='blog_view'),
)
