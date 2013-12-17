from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ms.views.home', name='home'),
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'flashcards/', include('flashcards.urls',namespace='flashcards')),
    url(r'^admin/', include(admin.site.urls)),
)
