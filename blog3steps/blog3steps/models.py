from django.db import models
from django.utils.translation import ugettext as _



class Blog(models.Model):
    """
    Simple class for managing Blog objects.
    Every Blog can have one or more Article instances related.
    """
    url = models.CharField(max_length=25, blank=False, verbose_name=_('url'), help_text=_('public URL of your Blog'))
    title = models.CharField(max_length=25, blank=False, verbose_name=_('title'), help_text=_('the "name" of your Blog'))
    administrator = models.CharField(max_length=50, blank=False, verbose_name=_('administrator'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))

    class Meta:
        ordering = ['-modified']    

    def __unicode__(self):
        return u'%s' % (self.url)
    
    @property
    def articles(self):
        return self.article_set.all()


class Article(models.Model):
    """
    Simple class for managing Article objects.
    """
    title = models.CharField(max_length=50, blank=False, verbose_name=_('title'))
    text = models.CharField(max_length=1000, blank=False, verbose_name=_('text'))
    author = models.CharField(max_length=50, blank=False, verbose_name=_('author'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))    
    blog = models.ForeignKey(Blog, blank=False, verbose_name=_('blog'))
    
    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u'%s' % (self.title)

