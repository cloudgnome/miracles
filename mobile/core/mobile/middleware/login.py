from mobile.views import SignUpView
from settings import AVAIL_LANGUAGES
from django.utils.translation import LANGUAGE_SESSION_KEY
from catalog.models import Product

class Login:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self,request,view,*args,**kwargs):
        if request.user.is_anonymous:
            return SignUpView.as_view()(request, *args,**kwargs)

        elif request.user.is_opt:
            Product.user = True
        else:
            Product.user = False

        return None