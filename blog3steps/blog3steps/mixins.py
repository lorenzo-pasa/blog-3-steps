from django.core.urlresolvers import reverse
from google.appengine.api import users

from .models import Blog



class AuthenticatedUserMixin(object):
    """
    Check if the user is authenticated via the Google APIs.
    If so, add some useful variables to the context.
    """
    def get_context_data(self, **kwargs):
        context = super(AuthenticatedUserMixin, self).get_context_data(**kwargs)        
        google_user = users.get_current_user()
        if google_user:
            user_id = google_user.user_id()
            try:
                blog = Blog.objects.get(administrator=user_id)
            except Blog.DoesNotExist:
                blog = None
            url_logout = users.create_logout_url(reverse('home'))
            context.update({
                'user_id': user_id,
                'blog': blog,
                'url_logout': url_logout
            })
        else:
            # At the moment, there is no need to manage unauthenticated users,
            # because every view with the AuthenticatedUserMixin is protected by
            # the "login: required" setting for URL handlers, in the app.yaml file.
            #
            # TODO: better management of the "unauthenticated user" case.
            pass
        return context

