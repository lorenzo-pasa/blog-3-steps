from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from .views import (AdminPanelView, ArticleListView, ArticleCreateView, 
                    ArticleUpdateView, ArticleDeleteView, BlogCreateView,
                    BlogUpdateView, BlogPublicView, WizardBlogCreateView,
                    WizardArticleCreateView)



urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),

    # Wizard URLs
    url(r'^wizard/2-steps-to-go/$', WizardBlogCreateView.as_view(), name='wizard_blog_create'),
    url(r'^wizard/1-step-to-go/$', WizardArticleCreateView.as_view(), name='wizard_article_create'),

    # Administration URLs    
    url(r'^administration/$', AdminPanelView.as_view(), name='admin_panel'),
    
    url(r'^administration/article-list/$', ArticleListView.as_view(), name='article_list'),
    url(r'^administration/article/add/$', ArticleCreateView.as_view(), name='article_add'),
    url(r'^administration/article/update/(?P<pk>\d+)/$', ArticleUpdateView.as_view(), name='article_update'),
    url(r'^administration/article/delete/(?P<pk>\d+)/$', ArticleDeleteView.as_view(), name='article_delete'),
    
    url(r'^administration/blog/add/$', BlogCreateView.as_view(), name='blog_add'),
    url(r'^administration/blog/update/(?P<pk>\d+)/$', BlogUpdateView.as_view(), name='blog_update'),

    # Public blog URLs    
    url(r'^(?P<blog_url>([a-z0-9]+[-]*)+[a-z0-9]+)/$', BlogPublicView.as_view(), name='blog_public'),
)

