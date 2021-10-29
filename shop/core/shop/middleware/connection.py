from shop.models import Connection
from django.http import HttpResponseForbidden,HttpResponsePermanentRedirect,Http404

class ConnectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        self.process_request(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_request(self,request):
        try:
            path = Connection.objects.get(url=request.path)
        except:
            path = Connection.objects.create(url=request.path)

        # if path.overloaded:
        #     raise Http404()

        path.limit += 1
        path.update()
