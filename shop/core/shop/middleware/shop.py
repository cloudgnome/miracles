from catalog.models import Product

class ShopMiddleware:
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
        if request.user.is_opt:
            Product.user = True
        else:
            Product.user = False

        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            request.folder = 'mobile'
        else:
            request.folder = 'desktop'
