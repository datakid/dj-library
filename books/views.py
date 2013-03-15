""" views.py
collects data to send to the templates

"""
from django.shortcuts import render_to_response, get_object_or_404
from library.books.models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from itertools import chain

## INDEXES ##

def index(request):
  """
  collects count on all books models: Source, Target, 
  Authors, Translators and languages for basic front page view
  """
  source_count = SourceText.objects.all().count()
  target_count = TargetText.objects.all().count()
  translator_count = Translator.objects.all().count()
  author_count = Author.objects.all().count()
  lang_dict = dict(LANGUAGES)
  langs = TargetText.objects.values_list('language', 
      flat=True).distinct().order_by('language')
  long_langs = [lang_dict[lang] for lang in langs]
  return render_to_response('library/index.html', locals()) 

def writer_index(request):
  """
  sends all author and translator data to template
  """
  all_authors = Author.objects.all()
  all_translators = Translator.objects.all() 
  return render_to_response('authors/index.html', locals()) 

def author_index(request):
  """
  sends all author data to template 
  """
  all_authors = Author.objects.all() 
  return render_to_response('authors/authors_index.html', locals()) 

def translator_index(request):
  """
  sends all translator data to template
  """
  all_translators = Translator.objects.all() 
  return render_to_response('authors/translators_index.html', locals()) 

def target_index(request):
  """
  sends all target texts to template
  """
  all_translations = TargetText.objects.all()
  return render_to_response('library/target_index.html', locals()) 

def source_index(request):
  """
  sends all source texts to template
  """
  all_sources = SourceText.objects.all()
  return render_to_response('library/source_index.html', locals()) 

def publisher_index(request):
  """
  sends all publishers to template
  """
  source_publishers = \
    SourceText.objects.values('publisher').distinct().order_by('publisher')
  target_publishers = \
    TargetText.objects.values('publisher').distinct().order_by('publisher')
  result_list = sorted(
      chain(source_publishers, target_publishers))
  return render_to_response('library/publishers_index.html', locals())

def tags_index(request):
  """
  sends all tags to template
  """
  source_count = SourceText.objects.all().count()
  target_count = TargetText.objects.all().count()
  translator_count = Translator.objects.all().count()
  author_count = Author.objects.all().count()
  lang_dict = dict(LANGUAGES)
  langs = TargetText.objects.values_list('language', 
      flat=True).distinct().order_by('language')
  long_langs = [lang_dict[lang] for lang in langs]
  return render_to_response('library/tags.html', locals())

def languages_index(request):
  """
  sends all target texts to template, ordered by language
  """
  all_targets = TargetText.objects.all().order_by('language','title')
  return render_to_response('library/languages_index.html', locals())  

## DETAILS ##

def author_detail(request, author_id):
  """
  sends data on particular author to template, books sorted by date
  """
  author = Author.objects.get(pk=author_id)
  books = author.sourcetext_set.all().order_by('date')
  return render_to_response('authors/author_detail.html', locals())

def translator_detail(request, translator_id):
  """
  sends data on particular translator to template, books sorted by date
  """
  translator = Translator.objects.get(pk=translator_id)
  books = translator.targettext_set.all().order_by('date')
  return render_to_response('authors/translator_detail.html', locals())

def book_detail(request, book_id):
  """
  sends particular book's detail to template
  """
  try:
    book = SourceText.objects.get(pk=book_id)
    targets = TargetText.objects.filter(source_text=book_id)
    return render_to_response('library/source_detail.html', locals())
  except SourceText.DoesNotExist:
    book = TargetText.objects.get(pk=book_id)
    return render_to_response('library/target_detail.html', {'book': book})

def source_detail(request, book_id):
  """
    sends source text detail to template
  """
  book = SourceText.objects.get(pk=book_id)
  targets = TargetText.objects.filter(source_text=book_id)
  return render_to_response('library/source_detail.html', locals())

def target_detail(request, book_id):
  """
    sends target text detail to template
  """
  book = TargetText.objects.get(pk=book_id)
  return render_to_response('library/target_detail.html', {'book': book})

def language_detail(request, language_id):
  """
    sends list of target texts to language template
  """
  for code, country in LANGUAGES:
    if country == language_id:
      this_country_code = code
  all_books_by_language = \
    TargetText.objects.filter(language=this_country_code).order_by('title')
  return render_to_response('library/language_detail.html', locals())

## FORMS ##

def source_form(request):
  """
    this is by the book - for when I've stopped abusing the admin interface 
  """
  if request.method == 'POST':
    form = SourceTextForm(request.POST)
    if form.is_valid():
      form.save()
  else:
    form = SourceTextForm()
  return render_to_response('library/source_form.html', {'form': form}, 
      context_instance=RequestContext(request))

def target_form(request):
  """
    this is by the book - for when I've stopped abusing the admin interface 
  """
  if request.method == 'POST':
    form = TargetTextForm(request.POST)
    if form.is_valid():
      form.save()
  else:
    form = TargetTextForm()
  return render_to_response('library/target_form.html', {'form': form}, 
      context_instance=RequestContext(request))

def statistics(request):
  """
  collects count on all books models: Source, Target, 
  Authors, Translators and languages for basic stats page view
  """
  source_count = SourceText.objects.all().count()
  ''' 
  target stats
  '''
  target_stats = TargetText.statistics.target_breakdown()
  '''
  translator stats
  '''
  translator_stats = Translator.statistics.translator_breakdown()
  target_count = TargetText.objects.all().count()
  translator_count = Translator.objects.all().count()
  
  author_count = Author.objects.all().count()
  lang_dict = dict(LANGUAGES)
  langs = TargetText.objects.values_list('language', flat=True).distinct().order_by('language')
  long_langs = [lang_dict[lang] for lang in langs]
  
  return render_to_response('library/stats.html', locals()) 

def german_texts(request):
  """
  renders all german target texts in alphabetical order
  """
  german_texts = TargetText.german.all()
  lang_dict = dict(LANGUAGES)
  langs = TargetText.objects.values_list('language', 
      flat=True).distinct().order_by('language')
  long_langs = [lang_dict[lang] for lang in langs]
  return render_to_response('library/german_index.html', locals()) 

def italian_texts(request):
  """
  renders all italian target texts in alphabetical order
  """
  italian_texts = TargetText.italian.all()
  lang_dict = dict(LANGUAGES)
  langs = TargetText.objects.values_list('language', 
      flat=True).distinct().order_by('language')
  long_langs = [lang_dict[lang] for lang in langs]
  return render_to_response('library/italian_index.html', locals()) 

def spanish_texts(request):
  """
  renders all spanish target texts in alphabetical order
  """
  spanish_texts = TargetText.spanish.all()
  lang_dict = dict(LANGUAGES)
  langs = TargetText.objects.values_list('language', 
      flat=True).distinct().order_by('language')
  long_langs = [lang_dict[lang] for lang in langs]
  return render_to_response('library/spanish_index.html', locals()) 

def japanese_texts(request):
  """
  renders all japanese target texts in alphabetical order
  """
  japanese_texts = TargetText.japanese.all()
  lang_dict = dict(LANGUAGES)
  langs = TargetText.objects.values_list('language', 
      flat=True).distinct().order_by('language')
  long_langs = [lang_dict[lang] for lang in langs]
  return render_to_response('library/japanese_index.html', locals()) 

def chineses_texts(request):
  """
  renders all chineses target texts in alphabetical order
  """
  chineses_texts = TargetText.chineses.all()
  lang_dict = dict(LANGUAGES)
  langs = TargetText.objects.values_list('language', 
      flat=True).distinct().order_by('language')
  long_langs = [lang_dict[lang] for lang in langs]
  return render_to_response('library/chineses_index.html', locals()) 

def chineset_texts(request):
  """
  renders all chineset target texts in alphabetical order
  """
  chineset_texts = TargetText.chineset.all()
  lang_dict = dict(LANGUAGES)
  langs = TargetText.objects.values_list('language', 
      flat=True).distinct().order_by('language')
  long_langs = [lang_dict[lang] for lang in langs]
  return render_to_response('library/chineset_index.html', locals()) 
