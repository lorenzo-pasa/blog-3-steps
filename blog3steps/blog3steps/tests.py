from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Blog, Article



## TESTS LIMITATIONS
#-------------------
#
# The "3 Steps Blog" project, so far, doesn't use the Django's authentication system,
# but relies on Google Accounts API for the users management.
#
# Due to this, it's not easy to create users for testing the views.
#
# Hence, some tests work from the opposite perspective:
# they check that, given an unauthenticated user, the view under test does NOT work as it
# should with an authenticated user.
#
# This limitation will be overcome in a future release.
#
# FURTHER NOTE:
# Actually, the app.yaml configuration forces the user to login before 
# accessing the application (except for the homepage).
# So, while using the application, it's impossible to be an unauthenticated user.
#
##



#-- Tests for models --#

class BlogModelTest(TestCase):

    def test_save_a_new_blog(self):
        blog = Blog.objects.create(
            url='unit-test-blog',
            title='Blog Testing',
            administrator='qwertyuiop1234567890'
        )
        blog.save()
        blog.full_clean()
        
        blog_list = Blog.objects.all()
        self.assertEqual(len(blog_list), 1)
        self.assertEqual(blog_list[0], blog)


class ArticleModelTest(TestCase):
  
    def test_save_a_new_article(self):
        blog_for_article = Blog.objects.create(
            url='unit-test-blog',
            title='Blog Testing',
            administrator='qwertyuiop1234567890'
        )
        blog_for_article.save()
        blog_for_article.full_clean()
        
        article = Article.objects.create(
            title='Test article',
            text='this is a test article',
            author=blog_for_article.administrator,
            blog=blog_for_article,
        )
        article.save()
        article.full_clean()
        
        article_list = Article.objects.all()
        self.assertEqual(len(article_list), 1)
        self.assertEqual(article_list[0], article)
        
        related_articles = blog_for_article.articles       
        self.assertEqual(len(related_articles), 1)
        self.assertEqual(related_articles[0], article)
        


#-- Tests for views --#

class BlogCreateViewTest(TestCase):

    def test_unauthenticated_user_is_NOT_redirected_to_update_blog_page(self):
        response = self.client.get(reverse('blog_add'), follow=True)
        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(response.redirect_chain, [])

                
class ArticleListViewTest(TestCase):

    def test_article_list_is_empty_when_current_user_is_unauthenticated(self):
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_list.html')      
        
        # "response.context['article_list']" belongs to the "Queryset" type,
        # hence "assertFalse" is used to check that it's empty.
        self.assertFalse(response.context['object_list'])      


class ArticleCreateViewTest(TestCase):

    def test_unauthenticated_user_is_redirected_to_article_list_page(self):
        response = self.client.get(reverse('article_add'), follow=True)
        self.assertRedirects(response, reverse('article_list'))    
        
        
        
#-- Tests for mixins --#

class AuthenticatedUserMixinTest(TestCase):
    
    def test_unauthenticated_user_does_NOT_have_additional_context_variables(self):
        response = self.client.get(reverse('admin_panel'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('user_id', response.context)
        self.assertNotIn('blog', response.context)
        self.assertNotIn('url_logout', response.context)                
        
        
