""" urls.py
the base url config. regexs to decipher uls, and the views they call
"""
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  (r'^$', include('library.books.urls')),  
  (r'^about/$', include('library.books.urls')),  
  (r'^library/', include('library.books.urls')),      
  (r'^admin/', include(admin.site.urls)),
  (r'^i18n/', include('django.conf.urls.i18n')),
)
