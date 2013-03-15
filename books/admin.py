""" admin.py 
  setup for the administration of the book app
"""
from library.books.models import SourceText, TargetText, Author, Translator 
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class AuthorsInline(admin.StackedInline):
  """ 
  set up so that athors are stacked inline 
  verbose_name here puts the correct name in the admin interface
  """
  model = SourceText.authors.through 
  verbose_name = _(u'Author') 
  verbose_name_plural = _(u'Authors')

class TranslatorsInline(admin.StackedInline):
  """ 
  set up so that translators are stacked inline
  verbose_name here puts the correct name in the admin interface
  """
  model = TargetText.translators.through 
  verbose_name = _(u'Translator') 
  verbose_name_plural = _(u'Translators')

class SourceTextAdmin(admin.ModelAdmin):
  """ display for ST admin """
  inlines = [
      AuthorsInline,
      ]
  exclude = ('authors',)
  fields = ['title', 'publisher', 'place', 'date', 'pages', 'book_tags']
  list_display = ('title', 'authors_names', 'date', 'publisher')
  search_fields = ['title', 'authors', 'date', 'book_tags']

class TargetTextAdmin(admin.ModelAdmin):
  """ Display for TT admin """
  inlines = [
      TranslatorsInline,
      ]
  exclude = ('translators',)
  fields = ['title', 'publisher', 'place', 'date', 'pages', 'book_tags', 
      'language', 'source_text']
  list_display = ('title', 'translators_names', 'date', 'language', 'publisher')
  search_fields = ['title', 'translators', 'language', 'book_tags']

class AuthorAdmin(admin.ModelAdmin):
  """ display """
  list_display = ['first', 'last']

class TranslatorAdmin(admin.ModelAdmin):
  """ display for Translator administration """
  list_display = ['first', 'last', 'name', 'language']

admin.site.register(SourceText, SourceTextAdmin)
admin.site.register(TargetText, TargetTextAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Translator, TranslatorAdmin)
