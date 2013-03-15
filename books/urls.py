""" urls.py
regex patterns for urls and which view to use
"""
from django.conf.urls.defaults import *
from django.contrib import admin
from library.books.models import SourceText
admin.autodiscover()

urlpatterns = patterns('library.books.views',
    (r'^$', 'index'),
    (r'^languages/$', 'languages_index'),
    (r'^languages/(?P<language_id>[a-zA-Z ]+)/$', 'language_detail'),
    (r'^targettexts/(?P<book_id>\d+)/$', 'target_detail'),
    (r'^targettexts/$', 'target_index'),
    (r'^sourcetexts/(?P<book_id>\d+)/$', 'source_detail'),
    (r'^sourcetexts/$', 'source_index'),
    (r'^about/$', 'index'),
    (r'^library/$', 'index'),
    (r'^books/$', 'index'),
    (r'^target_form/$', 'target_form'),
    (r'^source_form/$', 'source_form'),
    (r'^books/(?P<book_id>\d+)/$', 'book_detail'),
    (r'^authors/$', 'author_index'),
    (r'^authors/(?P<author_id>\d+)/$', 'author_detail'),
    (r'^translators/$', 'translator_index'),
    (r'^translators/(?P<translator_id>\d+)/$', 'translator_detail'),
    (r'^writers/$', 'writer_index'),
    (r'^publishers/$', 'publisher_index'),
    (r'^tags/$', 'tags_index'),
    (r'^statistics/$', 'statistics'),
    (r'^german/$', 'german_texts'),
    (r'^spanish/$', 'spanish_texts'),
    (r'^italian/$', 'italian_texts'),
    (r'^japanese/$', 'japanese_texts'),
    (r'^simplified chinese/$', 'chineses_texts'),
    (r'^traditional chinese/$', 'chineset_texts'),
)

urlpatterns += patterns('library.tagging.views',
    (r'^tag/(?P<tag>[^/]+)/$', 'tagged_object_list',
          dict(queryset_or_model=SourceText.objects.all())),
)
