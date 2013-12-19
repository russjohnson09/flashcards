from django.conf.urls import patterns, include, url

from django.contrib import admin

from flashcards import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^deck/$', views.index, name='index'),
    url(r'^deck/(?P<deck_id>\d+)/$', views.deckview, name='deck'),
    url(r'^card/(?P<card_id>\d+)/$', views.cardview, name='card'),
    url('^upload/$', views.upload, name='upload'),
    url('^export/(?P<deck_id>\d+)/$', views.export, name='export'),
    url('^review/(?P<deck_id>\d+)/$', views.review, name='review'),
    url('^ajax/', views.ajax, name='ajax'),
    #url(r'^ajax_json/', views.ajax_json, name='ajax_json'),
)
