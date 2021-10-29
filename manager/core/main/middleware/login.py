from main.views.login import SigninView

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
        if request.GET.get('username') and request.GET.get('password'):
            return None

        request.folder = 'desktop'
        if request.user.is_anonymous or not request.user.is_admin:
            return SigninView.as_view()(request)

        return None