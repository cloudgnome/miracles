from os.path import isfile
from settings import CACHE_URL

class Main:
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

        root = '{CACHE_URL}cache/html/desktop/ru/static/'.format(CACHE_URL=CACHE_URL)
        if not isfile(root + 'categories.html'):
            from catalog.views import StaticView
            StaticView(request,root)

        return None