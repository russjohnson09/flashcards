from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'flashcards/', include('flashcards.urls',namespace='flashcards')),
    url(r'blog/', include('blog.urls',namespace='blog')),
    url(r'bullets/', include('bullets.urls', namespace='bullets')),
)
