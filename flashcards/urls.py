from django.conf.urls import patterns, include, url

from django.contrib import admin

from flashcards import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^deck/$', views.index, name='index'),
    url(r'^deck/(?P<deck_id>\d+)/$', views.deck, name='deck'),
    url(r'^card/(?P<card_id>\d+)/$', views.card, name='card'),
)
