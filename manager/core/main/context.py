from settings import BASE_URL,SITE_URL,JS_BUILD,CSS_BUILD
from shop.models import Language
from main.models import Site

try:
    from settings import TIGRES_CATEGORIES
except:
    TIGRES_CATEGORIES = False

def extends(request):
    if request.is_ajax():
        return {'extends':'main/empty.html','BASE_URL':BASE_URL,'SITE_URL':SITE_URL}
    else:
        return {
            'extends':'main/index.html',
            'BASE_URL':BASE_URL,
            'SITE_URL':SITE_URL,
            'JS_BUILD':JS_BUILD,
            'CSS_BUILD':CSS_BUILD,
            'sites':Site.objects.filter(active=True),
            'TIGRES_CATEGORIES':TIGRES_CATEGORIES
        }