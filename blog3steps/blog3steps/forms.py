from django.forms import ModelForm, ValidationError, widgets
from django.utils.translation import ugettext as _

from .models import Article, Blog

import re



class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'text',)
        widgets = {
            'text': widgets.Textarea(attrs={'cols': 30, 'rows': 5}),
        }



class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ('url', 'title',)

    def clean_url(self):
    # Use the same regex used by the URLconf for matching the public blog URLs
        data = self.cleaned_data['url'].lower()
        check = re.match(r'^([a-z0-9]+[-]*)+[a-z0-9]+$', data)
        if not check:
            raise ValidationError(_("Only lowercase letters, numbers, or hyphens are admitted. It cannot start or end with a hyphen."))
        return data

