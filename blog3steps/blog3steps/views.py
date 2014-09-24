from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from google.appengine.api import users

from .forms import ArticleForm, BlogForm
from .mixins import AuthenticatedUserMixin
from .models import Article, Blog



class AdminPanelView(AuthenticatedUserMixin, TemplateView):
    template_name = "admin_panel.html"



#-- Article model's classes --#

class ArticleListView(AuthenticatedUserMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    
    def get_queryset(self):
        """
        Retrieve only Articles that belong to the current user.
        """
        queryset = super(ArticleListView, self).get_queryset()
        try:
            user_id = users.get_current_user().user_id()        
            blog = Blog.objects.get(administrator=user_id)
        except (AttributeError, Blog.DoesNotExist):
            blog = None
        queryset = queryset.filter(blog=blog)
        return queryset



class ArticleCreateView(AuthenticatedUserMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'form_article_add.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Prevent the creation of an Article by a user who doesn't have a Blog.
        """
        try:
            user_id = users.get_current_user().user_id()
            blog = Blog.objects.get(administrator=user_id)            
        except (AttributeError, Blog.DoesNotExist):
            return redirect(reverse('article_list'))
        else:
            return super(ArticleCreateView, self).dispatch(request, *args, **kwargs)        
    
    def form_valid(self, form):
        form.instance.author = users.get_current_user().user_id()
        form.instance.blog = Blog.objects.get(administrator=form.instance.author)
        return super(ArticleCreateView, self).form_valid(form)
            
    def get_success_url(self):
        return reverse('article_list')    



class ArticleUpdateView(AuthenticatedUserMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'form_article_update.html'
    
    def get_success_url(self):
        return reverse('article_list')
        


class ArticleDeleteView(AuthenticatedUserMixin, DeleteView):
    model = Article
    template_name = 'form_article_delete.html'
    
    def get_success_url(self):
        return reverse('article_list')

#-- end of Article classes --#



#-- Blog model's classes --#

class BlogCreateView(AuthenticatedUserMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name='form_blog_add.html'
    
    def dispatch(self, request, *args, **kwargs):
        """
        Prevents the creation of multiple Blog instances related to the same user.
        
        TODO: remove this override if a "multiple-blogs-per-user" feature will be implemented.
        """
        try:
            user_id = users.get_current_user().user_id()
            blog = Blog.objects.get(administrator=user_id)
        except (AttributeError, Blog.DoesNotExist):
            return super(BlogCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse('blog_update', kwargs={'pk':blog.pk}))

    def form_valid(self, form):
        google_user = users.get_current_user()
        if google_user:
            user_id = google_user.user_id()
        else:
            user_id = None    
        form.instance.administrator = user_id
        return super(BlogCreateView, self).form_valid(form)
        
    def get_success_url(self):
        return reverse('article_add')



class BlogUpdateView(AuthenticatedUserMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'form_blog_update.html'
    
    def get_success_url(self):
        return reverse('article_list')



class BlogPublicView(TemplateView):
    template_name="blog_public.html"    

    def get_context_data(self, **kwargs):
        context = super(BlogPublicView, self).get_context_data(**kwargs)
        try:
            user_id = users.get_current_user().user_id()
        except AttributeError:
            user_id = None        
        blog_url = self.kwargs.get('blog_url', None)
        blog = get_object_or_404(Blog, url=blog_url)
        context.update({
            'user_id': user_id,
            'blog': blog
        })        
        return context

#-- end of Blog classes --#



#-- All the classes for the Wizard steps --#

class WizardBlogCreateView(BlogCreateView):
    template_name='wizard/wizard_blog_add.html'

    def get_success_url(self):
        return reverse('wizard_article_create')



class WizardArticleCreateView(ArticleCreateView):
    template_name='wizard/wizard_article_add.html'

    def get_success_url(self):
        try:
            user_id = users.get_current_user().user_id()
            blog = Blog.objects.get(administrator=user_id)
        except (AttributeError, Blog.DoesNotExist):
            return reverse('admin_panel')
        else:
            return reverse('blog_public', kwargs={'blog_url':blog.url})

#-- end of the Wizard classes --#

