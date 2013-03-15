""" models.py 
    contains the models for:
    books, sourcetexts and translated texts
    authors, translators
"""
from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
import library.tagging
from library.tagging.fields import TagField

LANGUAGES = (
  (u'it', _(u'Italian')),
  (u'ja', _(u'Japanese')),
  (u'es', _(u'Spanish')),
  (u'zh-cn', _(u'Simplified Chinese')),
  (u'zh-tw', _(u'Traditional Chinese')),
  (u'fr', _(u'French')),
  (u'el', _(u'Greek')),
  (u'ar', _(u'Arabic')),
  (u'bg', _(u'Bulgarian')),
  (u'bn', _(u'Bengali')),
  (u'bs', _(u'Bosnian')),
  (u'ca', _(u'Catalan')),
  (u'cs', _(u'Czech')),
  (u'cy', _(u'Welsh')),
  (u'da', _(u'Danish')),
  (u'de', _(u'German')),
  (u'en', _(u'English')),
  (u'es-ar', _(u'Argentinean Spanish')),
  (u'et', _(u'Estonian')),
  (u'eu', _(u'Basque')),
  (u'fa', _(u'Persian')),
  (u'fi', _(u'Finnish')),
  (u'fy-nl', _(u'Frisian')),
  (u'ga', _(u'Irish')),
  (u'gl', _(u'Galician')),
  (u'he', _(u'Hebrew')),
  (u'hi', _(u'Hindi')),
  (u'hr', _(u'Croatian')),
  (u'hu', _(u'Hungarian')),
  (u'is', _(u'Icelandic')),
  (u'ka', _(u'Georgian')),
  (u'km', _(u'Khmer')),
  (u'kn', _(u'Kannada')),
  (u'ko', _(u'Korean')),
  (u'lt', _(u'Lithuanian')),
  (u'lv', _(u'Latvian')),
  (u'mk', _(u'Macedonian')),
  (u'nl', _(u'Dutch')),
  (u'no', _(u'Norwegian')),
  (u'pl', _(u'Polish')),
  (u'pt', _(u'Portuguese')),
  (u'pt-br', _(u'Brazilian Portuguese')),
  (u'ro', _(u'Romanian')),
  (u'ru', _(u'Russian')),
  (u'sk', _(u'Slovak')),
  (u'sl', _(u'Slovenian')),
  (u'sq', _(u'Albanian')),
  (u'sr', _(u'Serbian')),
  (u'sr-latn', _(u'Serbian Latin')),
  (u'sv', _(u'Swedish')),
  (u'ta', _(u'Tamil')),
  (u'te', _(u'Telugu')),
  (u'th', _(u'Thai')),
  (u'tr', _(u'Turkish')),
  (u'uk', _(u'Ukrainian')),
  (u'vi', _(u'Vietnamese')),
)

class Writer(models.Model):
  """ The underlying model for writers """
  first = models.CharField(_(u'First Name'), max_length=30)
  other = models.CharField(_(u'Other Names'), max_length=30, blank=True)
  last = models.CharField(_(u'Last Name'), max_length=30)
  dob = models.DateField(_(u'Date of Birth'), blank=True, null=True)

  class Meta:
    """ Some meta data """
    abstract = True
    ordering = ['last']
    unique_together = ("first", "last")

  def __unicode__(self):
    """ returns first last as the name """
    return u'%s %s' % (self.first, self.last)

class Author(Writer):
  """ Writers in English """
  language = models.CharField(_(u'language'), max_length=20, choices=LANGUAGES, blank=True)

  class Meta(Writer.Meta):
    """ Some meta data """
    verbose_name = _(u'Author')
    verbose_name_plural = _(u'Authors')

class TranslatorPercentManager(models.Manager):
  def translator_breakdown(self):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("""
      select language, count(*), (count(*)/(select count(*) from books_translator)*100) 
      from books_translator 
      group by language
      union
      select 'total', count(*), 100 
      from books_translator""")
    percent_list = []
    for row in cursor.fetchall():
      percent_list.append(row)
    return percent_list

class ItalianTranslatorManager(models.Manager):
  def get_query_set(self):
    return super(ItalianTranslatorManager,self).get_query_set().filter(language='it')

class JapaneseTranslatorManager(models.Manager):
  def get_query_set(self):
    return super(JapaneseTranslatorManager,self).get_query_set().filter(language='it')

class SpanishTranslatorManager(models.Manager):
  def get_query_set(self):
    return super(SpanishTranslatorManager,self).get_query_set().filter(language='it')

class GermanTranslatorManager(models.Manager):
  def get_query_set(self):
    return super(GermanTranslatorManager,self).get_query_set().filter(language='it')

class ChineseSTranslatorManager(models.Manager):
  def get_query_set(self):
    return super(ChineseSTranslatorManager,self).get_query_set().filter(language='it')

class ChineseTTranslatorManager(models.Manager):
  def get_query_set(self):
    return super(ChineseTTranslatorManager,self).get_query_set().filter(language='it')

class Translator(Writer):
  """ The translators """
  language = models.CharField(_(u'language'), max_length=20, choices=LANGUAGES)
  name = models.CharField(_(u'Source Name'), max_length=40, blank=True)  
  objects = models.Manager()
  statistics = TranslatorPercentManager()
  italian = ItalianTranslatorManager()
  chineseT = ChineseTTranslatorManager()
  chineseS = ChineseSTranslatorManager()
  japanese = JapaneseTranslatorManager()
  spanish = SpanishTranslatorManager()
  german = GermanTranslatorManager()

  class Meta(Writer.Meta):
    """ Some meta data """
    verbose_name = _(u'Translator')
    verbose_name_plural = _(u'Translators')
  
class Book(models.Model):
  """ the abstract book model """
  title = models.CharField(_(u'title'), max_length=100)
  publisher = models.CharField(_(u'publisher'), max_length=40)
  date = models.IntegerField(_(u'date'))
  place = models.CharField(_(u'place'), max_length=20)
  pages = models.IntegerField(_(u'pages'), blank=True, null=True)
  book_tags = TagField(_(u'book tags'))

  class Meta:
    """ Some meta data """
    ordering = ["title"]
    abstract = True
    verbose_name = _(u'Book')
    verbose_name_plural = _(u'Books')

  def __unicode__(self):
    return self.title

  def get_publisher(self):
    """ returns publisher """
    return self.publisher

  def get_place(self):
    """ returns place of publish """
    return self.place

  def get_date(self):
    """ returns date """
    return self.date

class SourceText(Book): 
  """ the source text (english) """
  language = models.CharField(_(u'language'), max_length=20, choices=LANGUAGES)
  authors = models.ManyToManyField(Author, verbose_name=_(u'List of Authors'))

  class Meta(Book.Meta):
    """ Some meta data """
    verbose_name = _(u'Source Text')
    verbose_name_plural = _(u'Source Texts')

  def authors_names(self):
    auth_list = self.authors.all()
    auth_string = ', '.join([str(p) for p in auth_list])
    return auth_string

try:
  library.tagging.register(SourceText)
except library.tagging.AlreadyRegistered:
  pass

class ItalianTargetManager(models.Manager):
  def get_query_set(self):
    return super(ItalianTargetManager,self).get_query_set().filter(language='it')

class JapaneseTargetManager(models.Manager):
  def get_query_set(self):
    return super(JapaneseTargetManager,self).get_query_set().filter(language='ja')

class SpanishTargetManager(models.Manager):
  def get_query_set(self):
    return super(SpanishTargetManager,self).get_query_set().filter(language='es')

class ChineseTTargetManager(models.Manager):
  def get_query_set(self):
    return super(ChineseTTargetManager,self).get_query_set().filter(language='zh-tw')

class ChineseSTargetManager(models.Manager):
  def get_query_set(self):
    return super(ChineseSTargetManager,self).get_query_set().filter(language='zh-cn')

class GermanTargetManager(models.Manager):
  def get_query_set(self):
    return super(GermanTargetManager,self).get_query_set().filter(language='de')

class TargetPercentManager(models.Manager):
  def target_breakdown(self):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("""
      select language, count(*), (count(*)/(select count(*) from books_targettext)*100) 
      from books_targettext 
      group by language
      union
      select 'total', count(*), 100 
      from books_targettext""")
    percent_list = []
    for row in cursor.fetchall():
      percent_list.append(row)
    return percent_list

class TargetText(Book):
  """ the translated text """
  language = models.CharField(_(u'language'), max_length=20, choices=LANGUAGES)
  source_text = models.ForeignKey(SourceText, related_name=_(u'source'), 
      verbose_name=_(u'Source Text'))
  translators = models.ManyToManyField(Translator, verbose_name=_(u'List of Translators'))
  objects = models.Manager()
  statistics = TargetPercentManager() 
  german = GermanTargetManager()
  japanese = JapaneseTargetManager()
  italian = ItalianTargetManager()
  spanish = SpanishTargetManager()
  chineset = ChineseTTargetManager()
  chineses = ChineseSTargetManager()

  class Meta(Book.Meta):
    """ Some meta data """
    verbose_name = _(u'Target Text')
    verbose_name_plural = _(u'Target Texts')

  def translators_names(self):
    auth_list = self.translators.all()
    auth_string = ', '.join([str(p) for p in auth_list])
    return auth_string
  
class SourceTextForm(ModelForm):
  """ the Form for entering SourceTexts """
  class Meta:
    """ Some meta data """
    model = SourceText

class TargetTextForm(ModelForm):
  """ the form for entering TargetTexts """
  class Meta:
    """ Some meta data """
    model = TargetText

