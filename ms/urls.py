from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'flashcards/', include('flashcards.urls',namespace='flashcards')),
)
