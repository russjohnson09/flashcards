from django.conf.urls import patterns, include, url

from bullets import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
