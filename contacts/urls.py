from django.conf.urls import patterns, include, url

from django.contrib import admin

from contacts import views
admin.autodiscover()

urlpatterns = patterns('',
    #main view
    url(r'^$', views.index, name='index'),
)
