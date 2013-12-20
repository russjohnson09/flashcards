from django.conf.urls import patterns, include, url

from django.contrib import admin

from flashcards import views
admin.autodiscover()

urlpatterns = patterns('',
    
    #main view. Displays user decks along with info on due dates, etc.
    url(r'^$', views.index, name='index'),

    #deck/card views
    url(r'^deck/(?P<deck_id>\d+)/$', views.deckview, name='deckview'),
    url(r'^card/(?P<card_id>\d+)/$', views.cardview, name='cardview'),
    url('^deck/(?P<deck_id>\d+)/import/$', views.deck_import, name='deck_import'),
    url('^deck/create/$', views.deck_create, name='deck_create'),
    url('^deck/(?P<deck_id>\d+)/edit$', views.deck_edit, name='deck_edit'),
    url('^deck/(?P<deck_id>\d+)/transfer$', views.deck_transfer, name='deck_transfer'),
    url('^export/(?P<deck_id>\d+)/$', views.deck_export, name='deck_export'),

    #review views
    url('^review/(?P<deck_id>\d+)/$', views.deck_review, name='deck_review'),
    url('^review/$', views.review, name='review'),
    
    #utility views
    url('^utils/$', views.utils, name='utils'),
    url('^utils/generate/$', views.utils_generate, name='utils_generate'),
    url('^utils/validate/$', views.utils_validate, name='utils_validate'),
    url('^utils/error/$', views.errorview, name='errorview'),
    #url('^ajax/$', views.ajax, name='ajax'),
    #url(r'^ajax_json/', views.ajax_json, name='ajax_json'),
)
